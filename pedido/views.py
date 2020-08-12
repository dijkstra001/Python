from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Caracteristica
from utils import utils
from .models import Pedido, Item

class DispatchLoginRequiredMixin(View):
    """
    Verifica se o usuário está logado. Isso impede que um usuário malicioso entre no pedido
    de outro usuário, sem autenticação de login.
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs

class PagarPedido(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'É necessário realizar login antes de prosseguir.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('cart'):
            messages.warning(
                self.request,
                'Agora seu carrinho vazio ;)'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('cart')
        caract_carrinho = [variacao for variacao in carrinho]
        bd_caract = list(
            Caracteristica.objects.select_related('produto').filter(id__in=caract_carrinho))

        for caract in bd_caract:
            caract_id = str(caract.id)
            estoque = caract.estoque
            qtd_carrinho = carrinho[caract_id]['quantidade']
            preco_unit = carrinho[caract_id]['preco_unitario']
            preco_unit_promo = carrinho[caract_id]['preco_promo']

            error_msg = ''

            if estoque < qtd_carrinho:
                carrinho[caract_id]['quantidade'] = estoque
                carrinho[caract_id]['preco_quantitativo'] = estoque * preco_unit
                carrinho[caract_id]['preco_quantitativo_promo'] = estoque * preco_unit_promo

                error_msg = 'Estoque insuficiente para alguns produtos do seu carrinho. Reduzimos a quantidade desses ' \
                            'produtos. Gentileza verificar as alteração a seguir. '

            if error_msg:
                messages.warning(
                    self.request,
                    error_msg
                )
                self.request.session.save()
                return redirect('produto:cart')

        qtd_total = utils.calcula_quantidade(carrinho)
        valor_total = utils.total_geral(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total,
            qtd_total=qtd_total,
            status='C',

        )
        pedido.save()

        Item.objects.bulk_create(
            [
                Item(
                    pedido=pedido,
                    produto=valor['produto_nome'],
                    produto_id=valor['produto_id'],
                    caracteristica=valor['variacao_nome'],
                    caracteristica_id=valor['variacao_id'],
                    preco=valor['preco_quantitativo'],
                    preco_promocional=valor['preco_quantitativo_promo'],
                    quantidade=valor['quantidade'],
                    imagem=valor['imagem'],

                ) for valor in carrinho.values()
            ]
        )

        messages.info(
            self.request,
            'Compra registrada com sucesso. Escolha o método de pagamento e calcule o frete para receber o seu pedido.'
        )
        del self.request.session['cart']

        # return render(self.request, self.template_name)

        return redirect(
            reverse(
                'pedido:pagar_pedido',
                kwargs={'pk': pedido.pk}

            )
        )

class DetalharPedido(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'

class ListaPedido(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista_pedido.html'
    paginate_by = 10
    ordering = ['-id']



