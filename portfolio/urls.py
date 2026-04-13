from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("blog-detail/", views.detail, name="blog-detail"),
    # path('about/', views.about, name='about'),
    # path('projects/', views.projects, name='projects'),
    # path('contact/', views.contact, name='contact'),
]
