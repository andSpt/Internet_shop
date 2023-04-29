from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView

from common.views import CommonMixin
from products.models import Basket
from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


class UserLoginView(CommonMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'

    def get_success_url(self):
        return reverse_lazy('index')


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированны!'
    title = 'Store - Регистрация'


class UserProfileView(CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class EmailVerificationView(CommonMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user,
                                                               code=code)
        print(type(email_verifications), email_verifications)
        if email_verifications.exists() and email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args,
                                                          **kwargs)
        else:
            HttpResponseRedirect(reverse('index'))
