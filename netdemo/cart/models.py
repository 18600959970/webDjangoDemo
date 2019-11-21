from django.db import models

# Create your models here.
from goods.models import *
from userapp.models import UserInfo
import math

class CartItem(models.Model):
    goodsid = models.PositiveSmallIntegerField()
    colorid = models.PositiveSmallIntegerField()
    sizeid = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ['goodsid','colorid','sizeid']

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getTotalPrice(self):
        return math.ceil(float(self.getGoods().price)*int(self.count))

