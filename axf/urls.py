from django.conf.urls import url

from axf import views

urlpatterns = [
    url(r'^$',views.home,name='index'), #首页
    url(r'^base/$',views.home,name='home'), #首页
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),  # 闪购超市
    url(r'^cart/$', views.cart, name='cart'),  # 购物车
    url(r'^mine/$', views.mine, name='mine'),  # 我的



    url(r'^register/$',views.register,name='register'),  #注册
    url(r'^checkaccount/$',views.checkaccount,name='checkaccount'), #帐号验证

    url(r'^logout/$',views.logout,name='logout'),  #退出
    url(r'^login/$',views.login,name='login'),   #登陆

    url(r'^addcart/$',views.addcart,name='addcart'), #添加购物车

    url(r'subcart/$',views.subcart,name='subcart') # 购物车减操作
]




