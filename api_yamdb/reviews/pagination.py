from rest_framework.pagination import PageNumberPagination


class ReviewsPagination(PageNumberPagination):
    page_size = 3


class CommentsPagination(PageNumberPagination):
    page_size = 4
