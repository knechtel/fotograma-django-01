from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm, SignUpForm
from .models import Comment, Like, Post


def feed(request):
    posts = Post.objects.select_related('author').annotate(like_count=Count('likes', distinct=True), comment_count=Count('comments', distinct=True))
    liked_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True)) if request.user.is_authenticated else set()
    return render(request, 'socialapp/feed.html', {'posts': posts, 'liked_ids': liked_ids, 'comment_form': CommentForm()})


def signup(request):
    if request.user.is_authenticated:
        return redirect('feed')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('feed')
    return render(request, 'socialapp/signup.html', {'form': form, 'eyebrow': 'BEM-VINDO AO FOTOGRAMA', 'heading': 'Sua conta começa aqui.', 'intro': 'Crie seu espaço e compartilhe os instantes que importam.', 'button': 'Criar minha conta'})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, 'Sua foto foi publicada!')
        return redirect('feed')
    return render(request, 'socialapp/create_post.html', {'form': form, 'eyebrow': 'UM NOVO INSTANTE', 'heading': 'Compartilhe sua foto.', 'intro': 'Escolha uma imagem e conte um pouco sobre ela.', 'button': 'Publicar foto'})


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.POST.get('next') or 'feed')


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user, comment.post = request.user, post
        comment.save()
    return redirect(request.POST.get('next') or 'feed')


def profile(request, username):
    from django.contrib.auth import get_user_model
    user = get_object_or_404(get_user_model(), username=username)
    posts = user.posts.select_related('author').annotate(like_count=Count('likes', distinct=True))
    return render(request, 'socialapp/profile.html', {'profile_user': user, 'posts': posts})
