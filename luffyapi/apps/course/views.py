from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend  # 过滤
from rest_framework.filters import OrderingFilter, SearchFilter  # 排序
from .paginations import PageNumberPagination
from . import serialiser
from . import models


#
class CourseCategoryView(GenericViewSet, ListModelMixin):
    """
    list:
        返回全部课程的分类
    """
    queryset = models.CourseCategory.objects.filter(is_show=True, is_delete=False).order_by('order')
    serializer_class = serialiser.CourseCategorySerializer


# 课程群查/单查
class CourseView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    list:
        返回全部课程

    retrieve:
        返回单个课程
    """
    queryset = models.Course.objects.filter(is_show=True, is_delete=False).order_by('order')
    serializer_class = serialiser.CourseModelSerializer
    # 分页
    pagination_class = PageNumberPagination
    # 过滤 排序
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id', 'students', 'price']
    filter_fields = ['course_category']  # 按课程过滤


# 课程章节课时
class CourseChapterView(GenericViewSet, ListModelMixin):
    """
    list:
        返回全部的章节+课时
    """
    queryset = models.CourseChapter.objects.filter(is_show=True, is_delete=False).order_by('order')
    serializer_class = serialiser.CourseChapterSerializer

    # 按课程过滤
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']  # 按课程过滤


# 搜索
class CourseSearchView(GenericViewSet, ListModelMixin):
    """
    list:
        返回搜索到的全部课程

    """
    queryset = models.Course.objects.filter(is_show=True, is_delete=False).order_by('order')
    serializer_class = serialiser.CourseModelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'keyword']
