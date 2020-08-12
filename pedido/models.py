from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Usuário')
    total = models.FloatField(default=0, verbose_name='Valor Total')
    qtd_total = models.PositiveIntegerField(default=0, verbose_name='Quantidade Total')
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
            ('X', 'Cancelado'),
        )
    )

    def __str__(self):
        return f'Pedido nº {self.pk}'

class Item(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Nº Pedido')
    produto = models.CharField(max_length=200, verbose_name='Produto')
    produto_id = models.PositiveIntegerField(verbose_name='ID do Produto')
    caracteristica = models.CharField(max_length=100, verbose_name='Característica')
    caracteristica_id = models.PositiveIntegerField(verbose_name='ID da Característica')
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(verbose_name='Preço Promocional')
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade')
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'


