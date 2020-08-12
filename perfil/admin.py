from django.contrib import admin
from . import models
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_nascimento', 'cpf', 'cidade', 'estado')
    list_display_links = ('id', 'usuario', )


admin.site.register(Perfil, PerfilAdmin)


