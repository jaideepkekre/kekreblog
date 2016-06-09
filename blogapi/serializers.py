from django.contrib.auth.models import User
from models import Blog, Comments
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class BlogSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('name', 'content', 'username')


class CommentsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('username', 'blog_name', 'content', 'parent')
