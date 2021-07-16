from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('change_password', views.change_password, name='change_password'),

    path("", views.list_symbol_asset, name="list_symbol_asset"),
    path("create-symbol-asset", views.create_symbol_asset, name="create_symbol_asset"),
    path("delete-symbol-asset", views.delete_symbol_asset, name="delete_symbol_asset"),


    path("crawl-symbol-info/", views.crawl_symbol_info, name="crawl_symbol_info"),
]
