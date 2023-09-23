from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_html_logo', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

    def get_html_logo(self, object):
        if object.logo:
            return mark_safe(f'<img src="{object.logo.url}" width=50>')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')
    search_fields = ('username',)

class CustomAdminSite(admin.AdminSite):
    def login(self, request, extra_context=None):
        if not request.user.is_authenticated:
            login_path = reverse('login')
            return HttpResponseRedirect(login_path)
        if self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)

admin_site = CustomAdminSite(name='customadminsite')

admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(User, UserAdmin)

admin_site.site_title = 'MiniStall administration'
admin_site.site_header = 'MiniStall administration'