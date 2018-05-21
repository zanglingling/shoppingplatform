from django.shortcuts import render
from django.views import View
from .models import OrderDetail, OrderMain
from myshop.models import ReceiverUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, HttpResponseBadRequest
from utils.error import StockException


class ShowOrder(LoginRequiredMixin, View):
    def get(self, request, oid):
        ordermain = OrderMain.objects.filter(pk=oid)
        receivers = ReceiverUser.objects.filter(receiveruser=request.user)
        orderdetails = OrderDetail.objects.filter(order=ordermain)
        return render(request, 'shop_order/place_order.html', locals())

    def post(self, reuqest, oid):
        receive = reuqest.POST.get('receiver_id')
        ordermain = OrderMain.objects.get(pk=oid)
        orderdetails = OrderDetail.objects.filter(order=ordermain)
        try:
            with transaction.atomic():
                for od in orderdetails:
                    if od.goods_info.stock < od.count:
                        raise StockException('%s库存不足' % od.goods_info.name)
                    od.goods_info.stock = F('stock') - od.count
                    od.goods_info.save()
                ordermain.receiver_id = receive
                ordermain.is_pay = '1'
                ordermain.total += 10
                ordermain.save()
        except StockException as e:
            ordermain.is_pay = '-1'
            ordermain.save()
            message = '%s，该订单被自动取消' % e
            return render(reuqest, 'shop_order/message.html', locals())
        message = '订单提交成功，请去支付'
        return render(reuqest, 'shop_order/message.html', locals())


class CancelOrder(View):
    def get(self, request):
        res = {'code': 0}
        order_id = request.GET.get('order_id')
        ordermain = OrderMain.objects.get(pk=order_id)
        if ordermain.user != request.user:
            return HttpResponseBadRequest()
        if ordermain.is_pay == '1':
            ordermain.is_pay = '-1'
            ordermain.save()
        else:
            res['code'] = -1
            res['message'] = '该订单无法取消'
        return JsonResponse(res)
