from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResultsSetPagination(PageNumberPagination):
    page_size = 30

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('num_page', self.page.paginator.num_pages),
            ('results', data)
        ]))
