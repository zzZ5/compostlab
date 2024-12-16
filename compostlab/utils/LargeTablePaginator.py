from django.core.paginator import Paginator


class LargeTablePaginator(Paginator):
    def _get_count(self):
        # 直接返回一个非常大的数字，而不是实际的行数
        return 100000000  # 设置一个足够大的数字

    count = property(_get_count)
