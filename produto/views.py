from django.shortcuts import render, redirect, reverse, get_object_or_404
from . import models
from perfil.models import Perfil
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6

class BuscaProdutos(ListaProdutos):
    template_name = 'produto/lista.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo') or self.request.session['termo']

        if not termo:
            return qs

        self.request.session['termo'] = termo
        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(resumo__icontains=termo) |
            Q(descricao__icontains=termo)
        )
        self.request.session.save()

        return qs

class DetalheProdutos(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AddCartProdutos(View):
    def get(self, *args, **kwargs):
        """if self.request.session.get('cart'):
            del self.request.session['cart']
            self.request.session.save()"""

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe :(',
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Caracteristica, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto
        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        preco_unitario = variacao.preco
        preco_promo = variacao.preco_promo
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Não há estoque disponível para o produto.'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        carrinho = self.request.session['cart']

        if variacao_id in carrinho:
            quantidade_atual = carrinho[variacao_id]['quantidade']
            quantidade_atual += 1

            if variacao_estoque < quantidade_atual:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_atual}x no produto {produto.nome}. '
                    f'Adicionamos {variacao_estoque}x no seu carrinho :)'
                )
                quantidade_atual = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_atual
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_atual
            carrinho[variacao_id]['preco_quantitativo_promo'] = preco_promo * quantidade_atual

        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_promo': preco_promo,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promo': preco_promo,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()
        messages.success(
            self.request,
            f' O produto {produto_nome} - [{variacao_nome}] foi adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)

class RemoveCartProdutos(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['cart']:
            return redirect(http_referer)

        carrinho = self.request.session['cart'][variacao_id]

        messages.success(
            self.request,
            f'O produto {carrinho["produto_nome"]} foi removido do seu carrinho.',
        )

        del self.request.session['cart'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)

class CartProdutos(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('cart', {})
        }

        return render(self.request, 'produto/carrinho.html', contexto)

class ResumoProdutos(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['cart'],

        }

        return render(self.request, 'produto/resumo.html', contexto)


