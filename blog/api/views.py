from rest_framework import viewsets
from blog.models import BlogPost
from .serializers import BlogPostSerializer
# from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . paginater import Paginater

class CRUD(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = Paginater

