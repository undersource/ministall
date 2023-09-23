from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import *
from .forms import *
from .serializers import *
from .monero_rpc import *
import mimetypes
import logging

logger = logging.getLogger(__name__)

class Index(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {'title': 'MiniStall', 'categories': Category.objects.all()}

class IndexAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class Search(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {'title': 'MiniStall - Search', 'categories': Category.objects.all()}

    def get_queryset(self):
        search_query = self.request.GET['q']
        return Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

class SearchAPI(ListAPIView):
    def get(self, request):
        search_query = request.GET['q']
        products = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        return Response({'products': ProductSerializer(products, many=True).data})

class CategoryView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {'title': 'MiniStall - Category', 'categories': Category.objects.all()}

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])

class CategoryAPIView(ListAPIView):
    def get(self, request):
        products = Product.objects.filter(category__slug=self.kwargs['category_slug'])
        return Response({'products': ProductSerializer(products, many=True).data})

class CategoryAPIList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class ProfileView(ListView):
    model = get_user_model()
    template_name = 'shop/profile.html'
    extra_context = {'title': 'MiniStall - Profile', 'categories': Category.objects.all()}

    def get_queryset(self):
        Profile = get_user_model()
        return Profile.objects.filter(username=self.request.user)

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404()

        context = super(ProfileView, self).get_context_data(**kwargs)

        return context

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = get_user_model().objects.get(username=request.user)
        balance = get_balance(user.monero_account_index) - user.spent
        return Response({'profile': {'username:': user.username, 'monero_address': user.monero_address, 'balance': float(balance)}})

class ProductView(DetailView):
    model = Product
    template_name = 'shop/payment.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    extra_context = {'title': 'MiniStall - Product'}

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404()

        context = super(ProductView, self).get_context_data(**kwargs)

        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    extra_context = {'title': 'MiniStall - Registration'}

    def form_valid(self, form):
        username = form.cleaned_data['username']

        account_index, address = create_account(username)

        user = form.save()
        login(self.request, user)

        account = get_user_model().objects.get(username=username)
        account.monero_account_index = account_index
        account.monero_address = address
        account.save()

        logger.info('{username} registred')

        return redirect('index')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'
    extra_context = {'title': 'MiniStall - Login'}

    def get_success_url(self):
        username = self.request.user.username
        logger.info('{username} logined')
        return reverse_lazy('index')

class ChangePassword(CreateView):
    form_class = ChangePasswordForm
    template_name = 'shop/password.html'
    extra_context = {'title': 'MiniStall - Change password'}

    def form_valid(self, form):
        username = self.request.user.username
        password = form.cleaned_data['oldpassword']
        newpassword = form.cleaned_data['newpassword1']
        user = authenticate(username=username, password=password)

        if user is not None:
            user.set_password(newpassword)
            user.save()

            logger.info('{username} changed password')

            return redirect('login')
        else:
            return render(self.request, 'shop/error.html', {'title': 'MiniStall - Error', 'error': 'Old password is incorrect'})

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404()

        context = super(ChangePassword, self).get_context_data(**kwargs)

        return context

class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        username = request.data['username']
        password = request.data['oldpassword']
        newpassword1 = request.data['newpassword1']
        newpassword2 = request.data['newpassword2']
        user = authenticate(username=username, password=password)
        status = str()

        if user is not None:
            if newpassword1 == newpassword2:
                user.set_password(newpassword1)
                user.save()

                logger.info('{username} changed password')

                status = 'Password been changed'
            else:
                status = "Two passwords didn't match"
        else:
            status = 'Old password is incorrect'

        return Response({'status': status})

class DeleteAccount(CreateView):
    form_class = DeleteAccountForm
    template_name = 'shop/unregister.html'
    extra_context = {'title': 'MiniStall - Delete account'}

    def form_valid(self, form):
        username=self.request.user.username
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        account = get_user_model().objects.get(username=username)

        if user is not None:
            account.delete()
            logger.info('{username} delete account')
            return redirect('index')
        else:
            return render(self.request, 'shop/error.html', {'title': 'MiniStall - Error', 'error': 'Invalid password'})

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404()

        context = super(DeleteAccount, self).get_context_data(**kwargs)

        return context

class DeleteAccountAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        account = get_user_model().objects.get(username=username)
        status = str()

        if user is not None:
            account.delete()
            logger.info('{username} delete account')
            status = 'Account has been deleted'
        else:
            status = 'Invalid password'

        return Response({'status': status})

def logout_user(request):
    username = request.user.username
    logout(request)
    logger.info('{username} logouted')
    return redirect('index')

def payment(request, product_slug):
    username = request.user.username

    get_object_or_404(get_user_model(), username=request.user)

    product = Product.objects.get(slug=product_slug)
    user = get_user_model().objects.get(username=request.user)
    price = product.price
    balance = get_balance(user.monero_account_index)
    spent = user.spent

    if balance - spent < price:
        return render(request, 'shop/error.html', {'title': 'MiniStall - Error', 'error': "You haven't money"})

    spent += price
    user.purchases.add(product)
    user.save()

    logger.info('{username} bought {product.slug}')

    return redirect('index')

def download(request, product_slug):
    username = request.user.username

    if not request.user.is_authenticated:
        raise Http404()

    product = Product.objects.get(slug=product_slug)
    filepath = product.product_file.path
    mime_type = mimetypes.guess_type(filepath)

    path = open(filepath, 'rb')

    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filepath

    logger.info('{username} download {product.slug}')

    return response