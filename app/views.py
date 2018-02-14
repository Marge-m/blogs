from django.views.generic import ListView, TemplateView, CreateView
from django.views.generic.edit import CreateView, FormView
from app.models import Blog, Post, Subscription, FinishedPost
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'home.html'


class BlogView(ListView):
    """
    User's blog
    """
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        user_id = self.kwargs['pk']
        blog = Blog.objects.get(user_id=user_id)
        posts = Post.objects.filter(blog_id=blog.pk)
        return posts

    def get_context_data(self, **kwargs):
        user_id = self.kwargs['pk']
        context = super(BlogView, self).get_context_data(**kwargs)
        context['bloguser'] = User.objects.get(pk=user_id)
        return context


class NewPostView(CreateView):
    template_name = 'newpost.html'
    model = Post
    fields = ['header', 'text', ]

    def form_valid(self, form):
        user_id = self.request.user.pk
        blog = Blog.objects.get(user_id=user_id)
        form.instance.blog_id = blog.pk
        response = super(NewPostView, self).form_valid(form)
        return response


class AllBlogsView(ListView):
    """
    All blogs
    """
    model = Blog
    template_name = 'all_blogs.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        blogs = Blog.objects.all()
        return blogs

    def get_context_data(self, **kwargs):
        user_id = self.request.user.pk
        context = super(AllBlogsView, self).get_context_data(**kwargs)
        try:
            subscriptions = Subscription.objects.values_list('blog_id', flat=True).filter(user_id=user_id)
        except:
            subscriptions = []
        context['subscriptions'] = subscriptions
        return context

    def post(self, request):
        if 'user_id' in self.request.POST:
            user_id = self.request.POST['user_id']
        else:
            user_id = request.user.pk
        if 'subscribe' in request.POST:
            blog_id = int(request.POST['subscribe'])
            Subscription.objects.create(user_id=user_id, blog_id=blog_id)
        else:
            blog_id = int(request.POST['unsubscribe'])
            subscription = Subscription.objects.get(user_id=user_id, blog_id=blog_id)
            subscription.delete()
        return HttpResponseRedirect('/allblogs')


class NewsFeedView(ListView):
    """
    News feed of a user
    """
    template_name = 'feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user_id = self.request.user.pk
        subscriptions = Subscription.objects.values_list('blog_id', flat=True).filter(user_id=user_id)
        posts = Post.objects.filter(blog_id__in=subscriptions).order_by('-date_created')
        return posts

    def get_context_data(self, **kwargs):
        user_id = self.request.user.pk
        finished = FinishedPost.objects.values_list('post_id', flat=True).filter(subscription__user_id=user_id)
        context = super(NewsFeedView, self).get_context_data(**kwargs)
        context['finished'] = finished
        return context

    def post(self, request):
        if 'user_id' in request.POST:
            user_id = request.POST['user_id']
        else:
            user_id = request.user.pk
        post = Post.objects.get(pk=int(request.POST['finished']))
        subscription = Subscription.objects.get(user_id=user_id,blog=post.blog)
        FinishedPost.objects.create(subscription=subscription, post=post)
        return HttpResponseRedirect('/feed')


class PostView(TemplateView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        post = Post.objects.get(pk=int(self.kwargs['pk']))
        context = super(PostView, self).get_context_data(**kwargs)
        context['header'] = post.header
        context['text'] = post.text
        context['created'] = post.date_created
        context['author'] = post.blog.user.username
        return context


