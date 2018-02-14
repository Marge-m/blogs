from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.db.models.signals import post_save


from app.models import Blog, Post, Subscription, FinishedPost
from app.views import NewsFeedView, AllBlogsView


class HomePageTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class BlogCreationTest(TestCase):
    """
    Test if user's Blog was created automatically after User creation
    """
    def setUp(self):
        user = User.objects.create_user(username='user', email='jane@doe.com', password='pass')
        self.user_id = user.pk

    def test_blog_creation(self):
        blog = Blog.objects.get(user=self.user_id)
        self.assertEquals(blog.user_id, self.user_id)


class TestMail(TestCase):
    """
    Test that mail is sent if new Post is created
    """
    def test_mail(self):
        with mock.patch('app.models.send_mail_if_post') as mocked_handler:
            post_save.connect(mocked_handler, sender=Post)
            # create new user object, subscribe it to itself and create 1 post in its blog
            user = User.objects.create_user(username='user2', email='jana@doe.com', password='pass2')
            subscription = Subscription.objects.create(user=user, blog=user.blog)
            post = Post.objects.create(blog=user.blog, header='header', text='text')
        self.assertEquals(mocked_handler.call_count, 1)


class NewsFeedPostFinished(TestCase):
    """
    Test if Post was actually mark as read if we marked it via News Feed
    """
    def setUp(self):
        self.view = NewsFeedView
        self.user = User.objects.create_user(username='user3', email='ja@doe.com', password='pass3')
        self.subscription = Subscription.objects.create(user=self.user, blog=self.user.blog)
        self.post = Post.objects.create(blog=self.user.blog, header='header', text='text')


    def test_post_marked_finished(self):
        view = resolve('/feed/')
        self.assertEquals(view.func.view_class, NewsFeedView)
        # create new user object, subscribe it to itself, create 1 post in its blog and mark it finished in Feed
        self.client.post('/feed/', {'finished': self.post.pk, 'user_id': self.user.pk})
        finished = FinishedPost.objects.filter(subscription=self.subscription, post=self.post).count()
        self.assertEquals(finished, 1)


class TestSubscription(TestCase):
    def setUp(self):
        self.view = AllBlogsView
        self.user = User.objects.create_user(username='user4', email='ja@doe.com', password='pass4')

    # test subscription and than unsuscription via button in News Feed
    def test_subscribe_unsubscribe(self):
        self.client.post('/allblogs/', {'user_id': self.user.pk, 'subscribe': self.user.blog.pk})
        subscription = Subscription.objects.filter(user_id=self.user.pk, blog=self.user.blog).count()
        self.assertEquals(subscription, 1)
        self.client.post('/allblogs/', {'user_id': self.user.pk, 'unsubscribe': self.user.blog.pk})
        subscription = Subscription.objects.filter(user_id=self.user.pk, blog=self.user.blog).count()
        self.assertEquals(subscription, 0)

