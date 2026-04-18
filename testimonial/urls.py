from django.urls import path
from . import views



urlpatterns = [
        path('', views.testimonial, name='testimonial'),
        path('create/', views.create_testimonial, name='create_testimonial'),
]