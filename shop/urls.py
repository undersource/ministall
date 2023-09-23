from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('search', Search.as_view(), name='search'),
    path('login', LoginUser.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('password', ChangePassword.as_view(), name='password'),
    path('unregister', DeleteAccount.as_view(), name='unregister'),
    path('logout', logout_user, name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('category/<slug:category_slug>', CategoryView.as_view(), name='category'),
    path('product/<slug:product_slug>', ProductView.as_view(), name='product'),
    path('payment/<slug:product_slug>', payment, name='payment'),
    path('download/<slug:product_slug>', download, name='download'),
    path('api/v1/index', IndexAPI.as_view()),
    path('api/v1/category/<slug:category_slug>', CategoryAPIView.as_view()),
    path('api/v1/categorylist', CategoryAPIList.as_view()),
    path('api/v1/search', SearchAPI.as_view()),
    path('api/v1/profile', ProfileAPIView.as_view()),
    path('api/v1/password', ChangePasswordAPI.as_view()),
    path('api/v1/unregister', DeleteAccountAPI.as_view())
]