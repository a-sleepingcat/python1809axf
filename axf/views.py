from django.shortcuts import render

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtypes, Goods


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

# categoryid 分类id
# childid子类id
#sortid 排序id
def market(request,categoryid,childid,sortid):  # 闪购超市

    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 分类点击下标 >>>分类id
    typeIndex = int(request.COOKIES.get('typeIndex',0)) #没有默认第o个
    # 根据分类下标 获取 对应 分类id
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames

    # 将每个子类拆分出来
    childTyplelist = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname':arr[0],  #子类名称
            'childid':arr[1],    #子类id
        }
        childTyplelist.append(dir)

        # 商品信息
        # goodsList = Goods.objects.all()[0:5]
    if childid == '0':  #全部分类
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:    #分类下子类
        goodsList = Goods.objects.filter(categoryid=categoryid, childid=childid)

    # 排序
    if sortid =='1':#销量排序
        goodsList = goodsList.order_by('-productnum')
    elif sortid =='2':#价格最低
        goodsList = goodsList.order_by('price')
    elif sortid =='3':#价格最高
        goodsList=goodsList.order_by(('-price'))
        
    data ={
        'foodtypes':foodtypes,   #分类信息
        'goodsList':goodsList,    #商品信息
        'childTyplelist':childTyplelist,   #子类信息
        'categoryid':categoryid,    #分类id
        'childid':childid,

    }
    return render(request,'market/market.html',context=data)


def cart(request):    # 购物车
    return render(request,'cart/cart.html')


def mine(request):   # 我的
    return render(request,'mine/mine.html')