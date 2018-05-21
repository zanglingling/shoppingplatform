from django.apps import AppConfig


class ShopOrderConfig(AppConfig):
    name = 'shop_order'
    verbose_name = '订单详情'

    def ready(self):
        import shop_order.signal
