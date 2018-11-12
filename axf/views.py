import hashlib
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtypes, Goods, User, Cart
from python1809axf import settings


def home(request):  # 首页
    # 轮播图数据
    wheels = Wheel.objects.all()

    # 导航数据
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shopList = Shop.objects.all()
    shophead = shopList[0]
    shoptab = shopList[1:3]
    shopclass = shopList[3:7]
    shopcommend = shopList[7:11]

    # 商品主体内容
    mainshows = Mainshow.objects.all()

    data = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys': mustbuys,
        'shophead':shophead,
        'shoptab':shoptab,
        'shopclass':shopclass,
        'shopcommend':shopcommend,
        'mainshows':mainshows
    }

    return render(request, 'home/home.html', context=data)

# categoryid 分类ID
# childid 子类ID
# sortid 排序ID
def market(request, categoryid, childid, sortid):    # 闪购超市
    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 分类 点击 下标  >>>>  分类ID
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据分类下标 获取 对应 分类ID
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames
    # 将每个子类拆分出来
    childTypleList = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname': arr[0],    # 子类名称
            'childid': arr[1]       # 子类ID
        }
        childTypleList.append(dir)

    # 商品信息 - 根据分类id获取对应数据
    # goodsList = Goods.objects.all()[0:5]
    if childid == '0':  # 全部分类
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:   # 分类 下 子类
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid)


    # 排序
    if sortid == '1':   # 销量排序
        goodsList = goodsList.order_by('-productnum')
    elif sortid == '2': # 价格最低
        goodsList = goodsList.order_by('price')
    elif sortid == '3': # 价格最高
        goodsList = goodsList.order_by(('-price'))

    # 购物车数据
    token = request.session.get('token')
    carts = []

    if token: #根据用户，获取对应用户下所有购物车数据
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)

    data = {
        'foodtypes':foodtypes,  # 分类信息
        'goodsList':goodsList,  # 商品信息
        'childTypleList': childTypleList,   # 子类信息
        'categoryid':categoryid,    # 分类ID
        'childid': childid,     # 子类ID
        'carts':carts,
    }

    return render(request, 'market/market.html', context=data)

# 购物车
def cart(request):
    token = request.session.get('token')
    if token: #有就显示购物车信息
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)
        return  render(request,'cart/cart.html',context={'carts':carts})
    else: #跳转到登陆页面
        return redirect('axf:login')

 # 我的
def mine(request):
    # 获取用户信息
    token = request.session.get('token')
    responseData = {

    }

    if token: #登陆
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank']= user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['isLogin'] = 1
    else:
        responseData['name'] ='未登录'
        # responseData['rank'] = '暂无等级'
        responseData['img'] = '/static/uploads/axf.png'

    return render(request, 'mine/mine.html',context=responseData)

# 加密
def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()

#注册
def register(request):
    if request.method == 'GET':
        return render(request,'mine/register.html')
    elif request.method =='POST':
       # try:
           user = User()
           user.account = request.POST.get('account')
           user.password = genarate_password(request.POST.get('password'))
           user.name = request.POST.get('name')
           user.phone = request.POST.get('phone')
           user.addr = request.POST.get('addr')
           # user.img = 'axf.png'

           # 头像
           imgName = user.account + '.png'
           imagePath = os.path.join(settings.MEDIA_ROOT, imgName)

           file = request.FILES.get('icon')
           # print(file.name)
           with open(imagePath, 'wb') as fp:
               for data in file.chunks():
                   fp.write(data)
           user.img = imgName

           user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

           user.save()

       #     状态保持
           request.session['token'] = user.token

       #     重定向
           return redirect('axf:mine')

       # except:
       #  return HttpResponse('注册失败')

#验证帐号
def checkaccount(request):
    account = request.GET.get('account')

    responseData = {
        'msg':'帐号可用',
        'status':1,    #1标识可用，-1标识为不可用
    }

    try:
        user = User.objects.get(account=account)
        responseData['msg'] = '帐号已被占用'
        responseData['status'] = -1
        return JsonResponse(responseData)
    except:
        return JsonResponse(responseData)

#退出
def logout(request):
    request.session.flush()
    return redirect('axf:mine')

#登陆
def login(request):
    if request.method =='GET':
        return render(request,'mine/login.html')
    elif request.method =='POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password == genarate_password(password): #密码相等，登录成功

                #更新token
                user.token = str(uuid.uuid5(uuid.uuid4(),'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')

            else:  #登陆失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误！'})
        except:
            return render(request,'mine/login.html',context={'accountErr':'帐号不存在！'})

# 添加购物车
def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'添加购物车成功',
        'status':1 #1标识添加成功，0标识添加失败，-1标识未登陆

    }
    if token : #登陆[直接操作模型]
        # 获取用户
        user = User.objects.get(token=token)
        # 获取商品
        goods = Goods.objects.get(pk=goodsid)

        # 商品已经在购物车，只改商品个数
        # 商品不存在购物车，新建对象（加入一条新的数据）
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists(): #修改数量
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number']= cart.number
        else: #添加一条新记录
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()
            responseData['number'] = cart.number
        return  JsonResponse(responseData)
    else:   #未登录[跳转到登陆页面]
        responseData['msg'] = '未登录，请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)

# 购物车删减操作
def subcart(request):
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    # 现实减号肯定的是登陆了，不要判断了
    # 对应用户和商品
    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk = goodsid)

    # 删减操作
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number -1
    cart.save()

    responseData = {
        'mag':'购物车减操作成功',
        'status':1,
        'number':cart.number
    }

    return JsonResponse(responseData)