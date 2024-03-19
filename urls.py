from django.urls import path
#from django.contrib.auth import views as auth_views
from . import views, viewscustomer, viewsordering, viewspopdf, viewsproductorder, viewsmerchandise, viewsProductPdf, viewsrequestresult, viewsdeposit 
from . import viewspayment, viewsdailyupdate, viewsindividualinvoice, viewsindiinvoicepdf,viewsinvoice,viewsinvoicepdf
# fileupload import
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve  #追加

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
    
    # 受発注実績一覧
    path('requestresult/list/', viewsrequestresult.RequestResultListView.as_view(), name='requestresultlist'),
    # 受発注実績登録
    #path('requestresult/new/<int:pk>/', viewsrequestresult.RequestResultCreateView.as_view(), name='requestresultnew'),
    # 受発注実績編集
    path('requestresult/edit/<int:pk>/', viewsrequestresult.RequestResultUpdateView.as_view(), name='requestresultedit'),
    # Ajax処理
    path("requestresult/edit/exec_result/", viewsrequestresult.RequestResultUpdateView.exec_ajax_result, name='exec_result'),
    # 更新Ajax処理
    #path("requestresult/edit/exec_renew/", viewsrequestresult.RequestResultUpdateView.as_view(), name='exec_renew'),

    # 受発注実績削除
    #path('requestresult/delete/<int:pk>/', viewsrequestresult.RequestResultDeleteView.as_view(), name='requestresultdelete'),
    # Ajax処理
    #path("requestresult/new/exec/", viewsrequestresult.RequestResultCreateView.exec_ajax, name='exec'),
    # 本番環境Media参照
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  #追加

    # 入金情報一覧
    path('deposit/list/', viewsdeposit.DepositListView.as_view(), name='Depositlist'),
    # 入金情報登録
    path('deposit/new/', viewsdeposit.DepositCreateView.as_view(), name='Depositnew'),
    # 入金情報編集
    path('deposit/edit/<int:pk>/', viewsdeposit.DepositUpdateView.as_view(), name='Depositedit'),
    # 入金情報削除
    path('deposit/delete/<int:pk>/',viewsdeposit.DepositDeleteView.as_view(),name='Depositdelete'),   

    # 支払情報一覧
    path('payment/list/', viewspayment.PaymentListView.as_view(), name='Paymentlist'),
    # 支払情報登録
    path('payment/new/', viewspayment.PaymentCreateView.as_view(), name='Paymentnew'),
    # 支払情報編集
    path('payment/edit/<int:pk>/', viewspayment.PaymentUpdateView.as_view(), name='Paymentedit'),
    # 支払情報削除
    path('payment/delete/<int:pk>/',viewspayment.PaymentDeleteView.as_view(),name='Paymentdelete'),   

    # 日次更新処理
    path('dailyupdate/new/', viewsdailyupdate.DailyUpdateView.as_view(), name='DailyUpdate'),

    # 個別請求書一覧
    path('individualinvoice/list/', viewsindividualinvoice.individualinvoiceListView.as_view(), name='individualinvoicelist'),
    # 個別請求書PDF出力
    path('individualinvoice/pdf/<int:pkfrom>/<int:pkto>/<int:isdate>/', viewsindiinvoicepdf.pdf, name='individualinvoicepdf'), 

    # 一括請求一覧
    path('invoice/list/', viewsinvoice.invoiceListView.as_view(), name='invoicelist'),
    # 一括請求書PDF出力
    path('invoice/pdf/<int:pkclosing>/<int:invoiceDate_From>/<int:invoiceDate_To>/', viewsinvoicepdf.pdf, name='invoicepdf'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 