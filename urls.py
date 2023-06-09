from django.urls import path
#from django.contrib.auth import views as auth_views
from . import views, viewscustomer, viewsordering, viewspopdf, viewsproductorder, viewsmerchandise

# fileupload import
from django.conf import settings
from django.conf.urls.static import static

app_name = "myapp"

urlpatterns = [
    path('', views.index, name='index'),  
    # signup
    path('signup/', views.signup, name='signup'),

    # 得意先仕入先一覧
    path('customersupplier/list/', viewscustomer.CustomerSupplierListView.as_view(), name='list'),
    # 得意先仕入先登録
    path('customersupplier/new/', viewscustomer.CustomerSupplierCreateView.as_view(), name='new'),
    # 得意先仕入先編集
    path('customersupplier/edit/<int:pk>/', viewscustomer.CustomerSupplierUpdateView.as_view(), name='edit'),
    # 得意先仕入先削除
    path('customersupplier/delete/<int:pk>/',viewscustomer.CustomerSupplierDeleteView.as_view(),name='delete'),   

    # 商品マスター一覧
    path('merchandise/list/', viewsmerchandise.MerchandiseListView.as_view(), name='merchandiselist'),
    # 商品マスター登録
    path('merchandise/new/', viewsmerchandise.MerchandiseCreateView.as_view(), name='merchandisenew'),
    # 商品マスター編集
    path('merchandise/edit/<int:pk>/', viewsmerchandise.MerchandiseUpdateView.as_view(), name='merchandiseedit'),
    # 商品マスター削除
    path('merchandise/delete/<int:pk>/',viewsmerchandise.MerchandiseDeleteView.as_view(),name='merchandisedelete'),   

    # 受発注一覧
    path('ordering/list/', viewsordering.OrderingListView.as_view(), name='orderinglist'),
    # 受発注登録
    path('ordering/new/', viewsordering.OrderingCreateView.as_view(), name='orderingnew'),
    # 受発注編集
    path('ordering/edit/<int:pk>/', viewsordering.orderingUpdateView.as_view(), name='orderingedit'),
    # 受発注削除
    path('ordering/delete/<int:pk>/', viewsordering.orderingDeleteView.as_view(), name='orderingdelete'),
    # PDF出力
    path('ordering/pdf/<int:pk>', viewspopdf.pdf, name='orderingpdf'), 

    # 製品発注一覧
    path('productorder/list/', viewsproductorder.ProductOrderListView.as_view(), name='productorderlist'),
    # 製品発注登録
    path('productorder/new/', viewsproductorder.ProductOrderCreateView.as_view(), name='productordernew'),
    # 製品発注編集
    #path('ordering/edit/<int:pk>/', viewsordering.orderingUpdateView.as_view(), name='orderingedit'),
    # 製品発注削除
    #path('ordering/delete/<int:pk>/', viewsordering.orderingDeleteView.as_view(), name='orderingdelete'),
    # PDF出力
    #path('ordering/pdf/<int:pk>', viewspopdf.pdf, name='orderingpdf'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)