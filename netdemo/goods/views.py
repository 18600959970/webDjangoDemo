from django.shortcuts import render

# Create your views here.
from django.views import View
from goods.models import *
from django.core.paginator import Paginator

class IndexView(View):
    def get(self,request,cid=1,num=1):
        cid = int(cid)
        num = int(num)
        # 查询所有类别的信息
        categorys = Category.objects.all().order_by('id')
        # 查询当前类别下的所有商品信息
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')

        # 分页（每页显示8条数据）
        pager = Paginator(goodsList,8)
        # 获取当前页的数据
        page_goodsList = pager.page(num)
        return render(request,'index.html',{'categorys':categorys,'goodsList':page_goodsList,'currentCid':cid})

def recommend_view(func):
    def wrapper(detailView,request,goodsid,*args,**kwargs):
        # 将存放在cookie中的goodsid获取
        cookie_list = request.COOKIES.get('recommend','')

        # 存有所有goodsid的列表
        goodsIdList = [gid for gid in cookie_list.split() if gid.strip()]
        # 最终需要获取的推荐商品
        goodsObjList = [Goods.objects.get(id=gsid) for gsid in goodsIdList if gsid!=goodsid and Goods.objects.get(id=gsid).category_id==Goods.objects.get(id=goodsid).category_id][:4]

        #将goodsObjList传递给get方法
        response = func(detailView,request,goodsid,goodsObjList,*args,**kwargs)

        # 判断goodsid是否存在goodsIdList中
        if goodsid in goodsIdList:
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0,goodsid)
        else:
            goodsIdList.insert(0,goodsid)
        # 将goodsIdList中的数据保存到cookie中
        response.set_cookie('recommend',' '.join(goodsIdList),max_age=3*60*60*24)
        return response
    return wrapper



class DetailView(View):
    @recommend_view
    def get(self,request,goodsid,recommendList=[]):
        goodsid = int(goodsid)
        # 根据gongsid查询商品的详情信息（goods对象）
        goods = Goods.objects.get(id=goodsid)
        return render(request,'detail.html',{'goods':goods,'recommendList':recommendList})