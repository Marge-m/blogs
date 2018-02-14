from django.contrib import admin

from .models import Blog, Post, Subscription, FinishedPost

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Subscription)
admin.site.register(FinishedPost)