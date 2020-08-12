from django.db import models
from PIL import Image
import os
from random import randint
from django.conf import settings
from django.contrib.auth.admin import messages
from django.utils.text import slugify
from utils import utils

class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome do Produto')
    resumo = models.TextField(verbose_name='Resumo do Produto')
    descricao = models.TextField(verbose_name='Descrição do Produto')
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m', verbose_name='Imagem do Produto')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_mkt = models.FloatField(verbose_name='Preço de Marketing')
    preco_promo = models.FloatField(default=0, verbose_name='Preço Promocional')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_mkt)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promo_formatado(self):
        return utils.formata_preco(self.preco_promo)
    get_preco_promo_formatado.short_description = 'Preço Promocional'

    @staticmethod
    def resize_image(img, new_width=200):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_heigth = img_pil.size

        if original_width <= new_width:
            print('Imagem não ajustada.')
            img_pil.close()
            return

        # Ajustando o tamanho da imagem:
        new_heigth = round((new_width * original_heigth) / original_width)
        new_img = img_pil.resize((new_width, new_heigth), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=70,
        )
        print('Imagem ajustada.')

    def save(self, *args, **kwargs):
        contador = randint(1000, 9999)
        if not self.slug:
            slug = f'{slugify(self.nome)}-{contador}'
            self.slug = slug

        super().save(*args, **kwargs)
        max_image_size = 200
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome


class Caracteristica(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto')
    nome = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome do Produto')
    preco = models.FloatField(verbose_name='Preço')
    preco_promo = models.FloatField(default=0, verbose_name='Preço Promocional')
    estoque = models.PositiveIntegerField(default=1, verbose_name='Estoque')

    def __str__(self):
        return self.nome or self.produto.nome
