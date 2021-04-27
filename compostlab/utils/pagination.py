from rest_framework.pagination import PageNumberPagination


class RecordPagination(PageNumberPagination):
    """
    Generate a custom definition pagination.
    """
    # url/?page=1&size=5
    page_query_param = 'page'
    page_size_query_param = 'size'

    def __init__(self, page_size=10, max_page_size=100) -> None:
        super().__init__()

        self.page_size = 10

        self.max_page_size = 100
