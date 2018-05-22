from django.shortcuts import render, redirect, reverse
from django.views import View
from .cache import ShoppingCarCache
from .models import ShoppingCar
from index.models import GoodsInfo
from shop_order.models import OrderMain, OrderDetail
from django.http import JsonResponse
from django.db import transaction
from utils.error import StockException
import uuid
from django.contrib.auth.views import redirect_to_login


class AddCarGoods(View):
    def get(self, request, did):
        buy_num = int(request.GET.get('buy_num'))
        if request.user.is_authenticated():
            # update_or_create 函数会返回两个参数
            # 第一个是你创建的实例
            # 第二个参数是当前实例是否为新建（新建为True,已存在为False）
            shopping_car_goods, is_now_create = ShoppingCar.objects.update_or_create(user=request.user, goods_id=did)
            shopping_car_goods.buy_num += buy_num
            shopping_car_goods.save()
            goods_num = ShoppingCar.objects.filter(user=request.user).count()

        else:
            # 获取cookie
            sessionid = request.COOKIES.get('mysessionid')
            # 实例化
            shoppingcarcache = ShoppingCarCache()
            # redis添加购物记录
            shoppingcarcache.add_car(sessionid, did, buy_num)
            goods_num = shoppingcarcache.hlen(sessionid)
        return JsonResponse({'code': 0, 'goods_num': goods_num})


class ShowCarGoods(View):
    def get(self, request):
        if request.user.is_authenticated():
            cart_goods = ShoppingCar.objects.filter(user=request.user)
        else:
            sessionid = request.COOKIES.get('mysessionid')
            shoppingcarcache = ShoppingCarCache()
            data = shoppingcarcache.hgetall(sessionid)
            cart_goods = []
            for did, buy_num in data.items():
                cart_goods.append({
                    'goods': GoodsInfo.objects.get(pk=did),
                    'buy_num': buy_num
                })

        return render(request, 'shop_cart/cart.html', locals())

    def post(self, request):
        if not request.user.is_authenticated():
            return redirect(reverse('account:login'))
            # return redirect_to_login(request.get_full_path())
        else:
            # 获取对应的checkbox类型的value，保存一个list类型的数据
            cart_by_goods_ids = request.POST.getlist('cart_by_goods_id')
            # 通过in_bulk，传入对应的id集合，则会返回对应的对象集合
            shop_carts = ShoppingCar.objects.in_bulk(id_list=cart_by_goods_ids)

            assert len(cart_by_goods_ids) == len(shop_carts.keys())
            try:
                with transaction.atomic():
                    ordermain = OrderMain(uuid=uuid.uuid4(), user=request.user, total=0)
                    ordermain.save()
                    total = 0
                    for goods in shop_carts.values():
                        orderdetail = OrderDetail()
                        orderdetail.order = ordermain
                        orderdetail.goods_info = goods.goods
                        orderdetail.goods_price = float(goods.goods.price)
                        if goods.buy_num > goods.goods.stock:
                            message = '%s库存不足' % goods.goods.name
                            raise StockException(message)
                        orderdetail.count = goods.buy_num
                        orderdetail.goods_total = float(goods.buy_num * goods.goods.price)
                        total += orderdetail.goods_total
                        orderdetail.save()
                        ShoppingCar.objects.filter(id=goods.id).delete()
                    ordermain.total = total
                    ordermain.save()
            except StockException as e:
                message = e
                cart_goods = ShoppingCar.objects.filter(user=request.user)
                return render(request, 'shop_cart/cart.html', locals())
            return redirect(reverse('shoppingorder:shoporder', kwargs={'oid': ordermain.id}))


class DelCarGoods(View):
    def get(self, request, gid):

        if request.user.is_authenticated():
            ShoppingCar.objects.filter(user=request.user, goods_id=gid).delete()
        else:

            sessionid = request.COOKIES.get('mysessionid')
            shoppingcarcache = ShoppingCarCache()
            shoppingcarcache.hdel(sessionid, gid)
        return JsonResponse({"code": 0})


class UpdateCarGoods(View):
    def get(self, request, gid):
        # 返回一个json字符串，格式如下： {"code": 0}
        #  code: 0为正常，1为库存不足
        buy_num = int(request.GET.get('buy_num'))
        res = {
            'code': 0
        }
        if buy_num:
            good_info = GoodsInfo.objects.get(pk=gid)
            if good_info.stock < buy_num:
                res['code'] = 1
                res['stock'] = good_info.stock
        if res['code'] == 0:
            if request.user.is_authenticated():
                ShoppingCar.objects.filter(user=request.user, goods_id=gid).update(buy_num=buy_num)
            else:
                sessionid = request.COOKIES.get('mysessionid')
                shoppingcarcache = ShoppingCarCache()
                shoppingcarcache.hupdate(sessionid, gid, buy_num)
            res['buy_num'] = buy_num
        return JsonResponse(res)
