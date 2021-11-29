from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import *
from .serializers import CategorySerializer, ReplySerializer, CommentSerializer, ProblemSerializer, \
    DepartmentSerializer, LikesSerializer, RatingSerializer, FavoriteSerializer
from .permissions import IsDepartmentAuthor



class PaginationClass(PageNumberPagination):
    page_size = 5
    # def get_paginated_response(self, data):
    #     for i in range(self.page_size):
    #         text = data[i]['description']
    #         data[i]['description'] = text[:55] + '...'
    #     return super().get_paginated_response(data)



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = PaginationClass

class DepartmentImageView(generics.ListCreateAPIView):
    queryset = DepartmentImage.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsDepartmentAuthor, ]
        else:
            permissions = []
        return [permission() for permission in permissions]



    def get_queryset(self):
        queryset = super().get_queryset()
        weeks = int(self.request.query_params.get('days', 0))
        if weeks > 0:
            start_date = timezone.now() - timedelta(days=weeks)
            queryset = queryset.filter(created_at__gte=start_date)
            return queryset

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = DepartmentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = DepartmentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsDepartmentAuthor, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class LikesViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer


class FavoriteViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class RatingViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer