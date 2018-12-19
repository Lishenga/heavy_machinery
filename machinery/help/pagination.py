from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination 

class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 0
    max_limit = 0

class PostPageNumberPagination(PageNumberPagination):
    page_size = 1

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000