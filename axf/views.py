from django.shortcuts import render

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, Mainshow


def home(request): #首页
    #轮播图数据
    wheels = Wheel.objects.all()

    # 导航数据
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    # 商品主体内容
    mainshows = Mainshow.objects.all()
    data = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptab':shoptab,
       'shopclass':shopclass,
        'shopcommend':shopcommend,
        'mainshows':mainshows,
    }

    return render(request,'home/home.html',context=data)

def market(request):  # 闪购超市
    return render(request,'market/market.html')


def cart(request):    # 购物车
    return render(request,'cart/cart.html')


def mine(request):   # 我的
    return render(request,'mine/mine.html')