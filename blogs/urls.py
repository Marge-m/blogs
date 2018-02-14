from django.contrib import admin
from app.views import BlogView, HomeView, NewPostView, AllBlogsView, NewsFeedView, PostView
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^allblogs/$', AllBlogsView.as_view(), name='all_blogs'),
    url(r'^blog/(?P<pk>\d+)/$', BlogView.as_view(), name='blog'),
    url(r'^newpost/$', NewPostView.as_view(), name='add_post'),
    url(r'^feed/$', NewsFeedView.as_view(), name='feed'),
    url(r'^post/(?P<pk>\d+)/$', PostView.as_view(), name='post'),
]
