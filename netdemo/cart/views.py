from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View
from cart.cartmanager import *

class AddCartView(View):
    def post(self,request):
        # 在多级字典数据的时候，需要手动是指modified=True，实时地将数据插入数据库
        request.session.modified = True
        #1.获取当前操作类型
        flag = request.POST.get('flag','')
        # 2.判断当前操作类型
        print(flag,'===============')
        if flag == 'add':
            #创建cartManager对象
            carManagerObj = getCartManger(request)
            # 加入购物车操作
            carManagerObj.add(**request.POST.dict())
            # print(carManagerObj,"++++++++++++++")
        elif flag == 'plus':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 修改商品的数量(添加)
            carManagerObj.update(step=1,**request.POST.dict())
        elif flag == 'minus':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 修改商品的数量(减)
            carManagerObj.update(step=-1,**request.POST.dict())
        elif flag == 'delete':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 删除商品
            carManagerObj.delete(**request.POST.dict())
        return HttpResponseRedirect('/cart/queryAll/')


class CartListView(View):
    def get(self,request):
        # 创建cartManager对象
        carManagerObj = getCartManger(request)
        # 查询所有购物信息
        cartList = carManagerObj.queryAll()
        # print(cartList)
        return render(request,'cart.html',{'cartList':cartList})