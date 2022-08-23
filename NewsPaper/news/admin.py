from django.contrib import admin
from .models import Author, Post, Category, PostCategory, Comment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
