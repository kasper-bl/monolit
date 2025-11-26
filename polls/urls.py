from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('create/', views.create_question, name ='create_question'),
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),
]