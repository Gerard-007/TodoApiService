from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from todos.pagination import CustomPageNumberPagination
from todos.serializers import TodoSerializer

from .models import Todo


class TodosAPIViews(ListCreateAPIView):
    serializer_class = TodoSerializer
    #Allows only authenticated users
    permission_classes=(IsAuthenticated,)
    #Use Custom Pagination instead of Default in settings....
    #eg: localhost:8000/app_list?p=num&count=num
    pagination_class=CustomPageNumberPagination
    #Filters...
    filter_backends=[DjangoFilterBackend, SearchFilter, OrderingFilter] # For django filters
    filterset_fields=['id', 'title', 'body', 'is_completed']
    search_fields=['id', 'title', 'body', 'is_completed']
    ordering_fields=['id', 'title', 'body', 'is_completed']

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes=(IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
