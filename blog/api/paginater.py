from rest_framework.pagination import PageNumberPagination

class Paginater(PageNumberPagination):
    page_size = 5