from django.contrib import admin
from . import models
from .models import Pedido, Item

class ItemInline(admin.TabularInline):
    model = models.Item
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = (ItemInline, )
    list_display = ('id', 'usuario', 'total', 'status', )
    list_display_links = ('id', 'usuario', )

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto', 'preco', 'quantidade', )
    list_display_links = ('id', 'pedido', )


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Item, ItemAdmin)
