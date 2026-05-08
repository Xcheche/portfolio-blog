from django.urls import path
from . import views


urlpatterns = [
    #----------------Portfolio app urls------------------#
    path("", views.home, name="home"),

    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('generate-share-link/<int:portfolio_id>/', views.generate_share_link, name='generate_share_link'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path("resume/", views.resume, name="resume"),
    path("share/<int:portfolio_id>/", views.share_portfolio, name="share_portfolio"),

   
]
