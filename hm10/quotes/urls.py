from django.urls import path
from quotes import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name='root'),
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('<int:page>', views.main, name='root_paginate'),
    path('scrape/', views.scrape_to_base, name='scrape_to_base'),
    path('author/<str:author_fullname>/', views.author_detail, name='author_details'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),

]