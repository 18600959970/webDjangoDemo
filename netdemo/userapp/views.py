from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.cartmanager import SessionCartManager
from utils.code import *
from userapp.models import UserInfo, Area, Address
from django.core.serializers import serialize

class ReisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        # 获取请求参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')
        # 插入数据库
        user = UserInfo.objects.create(uname=uname,pwd=pwd)
        # 判断是否注册成功
        if user:
            # 将用户信息存放至session对象中
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')


class CheckUnameView(View):
    def get(self,request):
        # 获取请求参数
        uname = request.GET.get('uname','')

        # 根据用户名去数据库中查
        userList = UserInfo.objects.filter(uname=uname)
        flag = False
        # 判断是否存在
        if userList:
            flag = True
        return JsonResponse({'flag':flag})


class CenterView(View):
    def get(self,request):
        return render(request,'center.html')


class LogoutView(View):
    def post(self,requset):
        # 删除session中登录用户信息
        if 'user' in requset.session:
            del requset.session['user']
        return JsonResponse({'delflag':True})


class LoginView(View):
    def get(self,request):
        # 获取请求参数
        red = request.GET.get('redirct','')
        print(red,'++++++')
        return render(request,'login.html',{'redirct':red})

    def post(self,request):
        #1.获取请求参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd', '')
        # 2.查询数据库中是否存在
        userList = UserInfo.objects.filter(uname=uname,pwd=pwd)
        if userList:
            request.session['user'] = userList[0]
            red = request.POST.get('redirect','')
            print(red,'=========')
            if red == 'cart':
                #将session中的购物项移动到数据库
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/cart/queryAll/')
            elif red == 'order':
                return HttpResponseRedirect('/order/order.html?cartitems='+request.POST.get('cartitems',''))
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')

class LoadCodeView(View):
    def get(self,request):
        img,str = gene_code()
        # 将生成的验证码存放到session中
        request.session['sessionCode'] = str
        return HttpResponse(img,content_type='image/png')


class CheckCodeView(View):
    def get(self,request):
        # 获取输入框中的验证码
        code = request.GET.get('code','')
        # 获取生成的验证码
        sessionCode = request.session.get('sessionCode',None)
        # 比较是否相等
        flag = code == sessionCode
        return JsonResponse({'checkFlag':flag})


class AddressView(View):
    def get(self,request):
        user = request.session.get('user', '')
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})

    def post(self,request):
        #获取请求参数
        aname = request.POST.get('aname','')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user','')
        # 将数据插入数据库
        address = Address.objects.create(aname=aname,aphon=aphone,addr=addr,userinfo=user,isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()))
        # 获取当前用户的所有收货地址
        addrList = user.address_set.all()
        return render(request,'address.html',{'addrList':addrList})


class LoadAreaView(View):
    def get(self,request):
        #获取请求参数
        pid = request.GET.get('pid',-1)
        pid = int(pid)
        # 根据父id查询区划信息
        areaList = Area.objects.filter(parentid=pid)
        # 进行序列化
        jareaList = serialize('json',areaList)
        return JsonResponse({'jareaList':jareaList})

