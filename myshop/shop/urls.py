from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='homepage'),
    path('register/', views.register, name='register'),
    path("login", views.login_request, name='login'),
    path("logout", views.logout_request, name="logout"),
    path('<category_slug>/', views.product_list, name= "all_list"),
    path('<category_slug>/<type_slug>', views.product_list, name='product_list_by_category'),
    path('<id>/<slug>/', views.product_detail, name='product_detail'),
    
]
