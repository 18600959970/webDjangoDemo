from django.db import models

# Create your models here.
class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return 'Category:%s'%self.cname

class Goods(models.Model):
    gname = models.CharField(max_length=100)
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5,decimal_places=2)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return 'Goods:%s'%self.gname

    # 获取商品的大图
    def getGImg(self):
        return self.inventory_set.first().color.colorurl

    # 获取商品所有颜色对象
    def getColorList(self):
        colorList = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colorList:
                colorList.append(color)
        return colorList

    def getSizeList(self):
        sizeList = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizeList:
                sizeList.append(size)
        return sizeList

    def getDetailList(self):
        import collections
        # 创建一个有序字典用于存放详情信息（key：详情名称，value：图片列表）
        datas = collections.OrderedDict()
        for goodsdetail in self.goodsdetail_set.all():
            # 获取详情名称
            gdname = goodsdetail.name()
            print(gdname)
            if gdname not in datas:
                datas[gdname] = [goodsdetail.gdurl]
            else:
                datas[gdname].append(goodsdetail.gdurl)
        return datas

class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

    def __str__(self):
        return 'GoodsDetailName:%s'%self.gdname

class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    gdname = models.ForeignKey(GoodsDetailName,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

    # 获取详情名称
    def name(self):
        return self.gdname.gdname
class Size(models.Model):
    sname = models.CharField(max_length=10)

    def __str__(self):
        return 'Size:%s'%self.sname

class Color(models.Model):
    colorname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to='color/')

    def __str__(self):
        return 'Color:%s'%self.colorname

class Inventory(models.Model):
    count = models.PositiveSmallIntegerField()
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
