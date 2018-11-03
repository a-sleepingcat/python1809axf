from django.shortcuts import render

# Create your views here.


def home(request): #首页
    #轮播图数据
    return render(request,'home/home.html')

def market(request):  # 闪购超市
    return render(request,'market/market.html')


def cart(request):    # 购物车
    return None


def mine(request):   # 我的
    return None