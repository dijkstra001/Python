from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from . import models, forms
from django.contrib.messages.views import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
import copy


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('cart', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(usuario=self.request.user).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil),
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform': forms.PerfilForm(data=self.request.POST or None),
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class CriarPerfil(BasePerfil):
    def post(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se os campos foram preenchidos corretamente.'
            )
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # Usuário logado: atualização
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            messages.success(
                self.request,
                'Usuário atualizado com sucesso.'
            )

            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                print(self.perfilform.cleaned_data)
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # Usuário não logado (novo):
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            messages.success(
                self.request,
                f'O usuário {usuario} foi criado com sucesso.'
            )

        if password:
            autenticacao = authenticate(
                self.request,
                username=usuario,
                password=password,
            )
            if autenticacao:
                login(self.request, user=usuario)

        self.request.session['cart'] = self.carrinho
        self.request.session.save()
        if not self.request.session.get('cart'):
            return redirect('produto:lista')

        return redirect('produto:cart')


class AtualizarPerfil(View):
    def get(self, *args, **kwargs):
        return redirect('perfil:criar')


class LoginPerfil(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        autenticacao = authenticate(self.request, username=username, password=password)

        if not autenticacao:
            messages.error(
                self.request,
                'Usuário não existe. Gentileza realizar o cadastro.'
            )
            return redirect('perfil:criar')

        login(self.request, user=autenticacao)

        messages.success(
            self.request,
            f'Login efetuado com sucesso. Olá, {self.request.user.first_name}!'
        )
        if not self.request.session.get('cart'):

            return redirect('produto:lista')

        return redirect('produto:cart')


class LogoutPerfil(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('cart', {}))
        logout(self.request)
        self.request.session['cart'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')
