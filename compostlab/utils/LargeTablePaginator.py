from django.core.cache import cache
from django.core.paginator import Paginator


class LargeTablePaginator(Paginator):
    def _get_count(self):
        # 尝试从缓存中获取 count 值
        count = cache.get("data_count")
        if count is None:
            # 如果缓存中没有 count，则从数据库中计算 count 并缓存
            count = self.object_list.count()
            # 设置缓存过期时间为 5 小时（5 * 60 * 60 秒）
            cache.set("data_count", count, timeout=5 * 60 * 60)
        return count

    count = property(_get_count)
