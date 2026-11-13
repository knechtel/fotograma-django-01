from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('cadastro/', views.signup, name='signup'),
    path('entrar/', auth_views.LoginView.as_view(template_name='socialapp/login.html', extra_context={'eyebrow': 'QUE BOM TER VOCÊ DE VOLTA', 'heading': 'Entre no seu canto.', 'intro': 'Acesse sua conta para acompanhar a comunidade.', 'button': 'Entrar'}), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('publicar/', views.create_post, name='create_post'),
    path('curtir/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comentar/<int:post_id>/', views.add_comment, name='add_comment'),
    path('perfil/<str:username>/', views.profile, name='profile'),
]
