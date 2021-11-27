from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user_index/<int:num>/', views.user_index, name='user_index'),
    path('user_detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('match_index/<int:num>/', views.match_index, name='match_index'),
    path('match_detail/<int:pk>/', views.match_detail, name='match_detail'),
    path('submit_deck/<int:pk>/', views.submit_deck, name='submit_deck'),
    path('register_match/', views.register_match, name='register_match'),
    path('submit_result/<int:pk>/', views.submit_result, name='submit_result'),
    path('edit_match/<int:pk>/', views.edit_match, name='edit_match'),
    path('delete_match/<int:pk>/', views.delete_match, name='delete_match'),
    path('deckthema_index/', views.deckthema_index, name='deckthema_index'),
    path('deckthema_detail/<int:pk>/', views.deckthema_detail, name='deckthema_detail'),
    path('deck_records/', views.deck_records, name='deck_records'),
    path('rank/', views.rank, name='rank'),
]
