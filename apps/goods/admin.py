from django.contrib import admin
from django.core.cache import cache
from goods.models import GoodsType,GoodsSKU,Goods,IndexTypeGoodsBanner,IndexPromotionBanner,IndexGoodsBanner
# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request, obj)
        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')


class GoodsTypeAdmin(BaseModelAdmin):
    list_per_page = 3
    actions_on_top = False
    actions_on_bottom = True
    list_display = ["id", "name", "logo", "image", "addname"]
    list_filter = ['name']
    search_fields = ["name", "logo"]


class GoodsAdmin(BaseModelAdmin):
    list_per_page = 3
    actions_on_top = False
    actions_on_bottom = True
    list_display = ["id", "name"]

class GoodsSKUAdmin(BaseModelAdmin):
    list_per_page = 3
    actions_on_top = False
    actions_on_bottom = True
    list_display = ["id", "name"]

class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexTypeGoodsBannerAdmin(BaseModelAdmin):
    list_per_page = 3
    actions_on_top = False
    actions_on_bottom = True
    list_display = ["type", "sku", "display_type", "index"]


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)

