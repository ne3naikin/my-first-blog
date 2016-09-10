from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk) # якщо поста нема видае страницю з вказівкою що її нема, тобто 404
    
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    
    if request.method == "POST":
        form = PostForm(request.POST) # якщо пост вже написаний
        if form.is_valid(): # перевірка всі дані попали в пост перед тим як їого зберегти
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk) # перекидає після збереження посту на цю сторінку з відображеням тількі що написаному посту
    else:
        form = PostForm() # якщо пост тільки створюєтся

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk) 

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

# Create your views here.