from django.contrib import admin
from .models import Produto, Caracteristica
from . import models
from django_summernote.admin import SummernoteModelAdmin

class CaracteristicaInline(admin.TabularInline):
    model = models.Caracteristica
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    inlines = (CaracteristicaInline, )
    list_display = ('id', 'nome', 'slug', 'get_preco_formatado', 'get_preco_promo_formatado', 'tipo')
    list_display_links = ('id', 'nome', )


class CaracteristicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'nome', 'preco', 'preco_promo', 'estoque')
    list_display_links = ('id', 'produto', 'nome', )


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Caracteristica, CaracteristicaAdmin)

