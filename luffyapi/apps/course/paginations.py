from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination


class PageNumberPagination(DRFPageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    max_page_size = 10  # 页面的最大大小
    page_size_query_param = 'page_size'  # 前端可以指定页面大小
