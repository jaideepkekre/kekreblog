import hashlib

from django.contrib.auth.models import User
from models import Blog, Comments
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from serializers import BlogSerilizer, CommentsSerilizer, UserSerializer


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@renderer_classes((BrowsableAPIRenderer,))
def create_user(request):
    """
    Expects : {"username": "example@mail.com","password": "secret"}\n
    1. Registers Users\n
    2. Does NOT allow same username to be repeated\n
    3. Password stored as HASH
    4. If registered HTTP_201 else HTTP_412
    """

    if request.method == 'POST':

        queryset = User.objects.all()
        serializer = UserSerializer(data=request.data)
        new_username = request.data['username']
        password = request.data['password']

        for users in queryset:
            if new_username == users.username:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        if serializer.is_valid():
            serializer.save(password=hashlib.sha224(password).hexdigest())
            print ("User registered : " + str(serializer.data))

            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@renderer_classes((BrowsableAPIRenderer,))
def login_user(request):
    """
    Expects :{"username": "example@mail.com","password": "secret"}

    1.logs in Users

    2.If login okay , HTTP_200 else HTTP_403
    """

    if request.method == 'POST':

        queryset = User.objects.all()
        serializer = UserSerializer(data=request.data)
        new_username = request.data['username']
        password = hashlib.sha224(request.data['password']).hexdigest()

        for users in queryset:
            if new_username == users.username:
                if password == users.password:
                    return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@renderer_classes((BrowsableAPIRenderer,))
def create_blog(request):
    """
    Expects:{"username":"example@mail.com","name":"Default","content":"This is some HTML"}\n

    1.Creates article for user\n
    2.Ensures unique blog name , can be replaced by an custom ID field to allow duplicate blogs\n

    TODO : Verify user login via session
    """

    if request.method == 'POST':

        queryset = Blog.objects.all()
        serializer = BlogSerilizer(data=request.data)
        new_blog = request.data['name']

        for blogs in queryset:
            if new_blog == blogs.name:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@renderer_classes((BrowsableAPIRenderer,))
def update_blog(request):
    """
    Expects:{"username":"example@mail.com","name":"Default","content":"This is some HTML"}\n

    1.Updates article for user\n
    2.Ensures unique blog name , (can be replaced by an custom ID field to allow duplicate blogs)\n
    3.Checks if the blogs username is registered
    4.Checks if the owner of the article in request is actually the owner

    TODO : Verify user login via session / Use PUT instead of POST / Use Partial update
    """

    if request.method == 'POST':

        queryset = Blog.objects.all()
        serializer = BlogSerilizer(data=request.data)
        updated_blog = request.data['name']
        userset = User.objects.all()

        for user in userset:
            if user.username == request.data['username']:
                for blogs in queryset:
                    if updated_blog == blogs.name:
                        if blogs.username == request.data['username']:
                            if serializer.is_valid():
                                blog_id = blogs.id
                                blog_obj = Blog(id=blog_id, name=updated_blog, content=request.data['content'],
                                                username=request.data['username'])
                                blog_obj.save(force_update=True)
                                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_412_PRECONDITION_FAILED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@renderer_classes((BrowsableAPIRenderer,))
def delete_blog(request):
    """
    Expects:{"username":"example@mail.com","name":"Default","content":"This is some HTML"}\n

    1.Deletes article .\n


    TODO : Verify user login via session / Use DELETE instead of POST
    """

    if request.method == 'POST':

        queryset = Blog.objects.all()
        serializer = BlogSerilizer(data=request.data)
        deleted_blog = request.data['name']
        for blogs in queryset:
            print (str(blogs.name))
            if deleted_blog == blogs.name:
                if serializer.is_valid():
                    blogs.delete()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_412_PRECONDITION_FAILED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@renderer_classes((BrowsableAPIRenderer,))
def create_comment(request):
    """
    Expects : {"username": "example@mail.com","content": "this is nice ","blog_name":"Default","parent":0}\n
    1. Creates comments\n
    2. Does NOT allow comments for non existent blogs\n
    3. If successful HTTP_201 else HTTP_412
    """

    if request.method == 'POST':

        queryset = Comments.objects.all()
        serializer = CommentsSerilizer(data=request.data)

        blog_name = request.data['blog_name']
        blogset = Blog.objects.all()
        for blogs in blogset:
            if blog_name == blogs.name:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_412_PRECONDITION_FAILED)
