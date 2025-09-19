from django.urls import path
from . import views

urlpatterns = [
    path('', views.petition_list, name='petition_list'),
    path('create/', views.create_petition, name='create_petition'),
    path('<int:petition_id>/', views.petition_detail, name='petition_detail'),
    path('<int:petition_id>/vote/', views.vote_petition, name='vote_petition'),
]
