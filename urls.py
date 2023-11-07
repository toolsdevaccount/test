from django.urls import path
#from django.contrib.auth import views as auth_views
from . import views, viewscustomer, viewsordering, viewspopdf, viewsproductorder, viewsmerchandise, viewsProductPdf, viewsrequestresult

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
    # Ajax処理
    path("productorder/new/exec/", viewsproductorder.ProductOrderCreateView.exec_ajax, name='exec'),
    # 製品発注編集
    path('productorder/edit/<int:pk>/', viewsproductorder.ProductOrderUpdateView.as_view(), name='productorderedit'),
    # 製品発注削除
    path('productorder/delete/<int:pk>/', viewsproductorder.ProductOrderDeleteView.as_view(), name='productorderdelete'),
    # PDF出力
    path('productorder/pdf/<int:pk>', viewsProductPdf.pdf, name='productorderpdf'),
    
    # 受発注一覧
    path('requestresult/list/', viewsrequestresult.RequestResultListView.as_view(), name='requestresultlist'),
    # 受発注登録
    path('requestresult/new/<int:pk>/', viewsrequestresult.RequestResultCreateView.as_view(), name='requestresultnew'),
    # 受発注編集
    path('requestresult/edit/<int:pk>/', viewsrequestresult.RequestResultUpdateView.as_view(), name='requestresultedit'),
    # 受発注削除
    path('requestresult/delete/<int:pk>/', viewsrequestresult.RequestResultDeleteView.as_view(), name='requestresultdelete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 