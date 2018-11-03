from django.db import models

# Create your models here.

# 基础类
class Base(models.Model):
    # 图片
    img = models.CharField(max_length=100)
    # 名称
    name = models.CharField(max_length=100)
    # 商品编号
    trackid = models.CharField(max_length=10)

    class Meta:
        abstract = True

