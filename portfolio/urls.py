from django.urls import path
from . import views


urlpatterns = [
    #----------------Portfolio app urls------------------#
    path("", views.home, name="home"),
    #path("blog-detail/", views.detail, name="blog-detail"),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),

   
]
