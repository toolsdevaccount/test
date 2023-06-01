from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView
from .models import ProductOrder
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q
# 日時
#from django.utils import timezone
#import datetime
# forms
from .formsproductorder import ProductOrderForm
# Transaction
from django.db import transaction
# fileupload
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# 受発注一覧/検索
class ProductOrderListView(LoginRequiredMixin,ListView):
    model = ProductOrder
    form_class = ProductOrderForm
    context_object_name = 'object_list'
    queryset = ProductOrder.objects.order_by('ProductOrderOrderingDate','Created_at').reverse()
    template_name = "crud/productorder/List/productorderlist.html"
    paginate_by = 10

    #検索機能
    def get_queryset(self):
        # 依頼日大きい順で抽出
        queryset = ProductOrder.objects.order_by('ProductOrderOrderingDate','Created_at').reverse()
        # 削除済除外
        queryset = queryset.filter(is_Deleted=0)
        query = self.request.GET.get('query')      
        productorderdateFrom = self.request.GET.get('productorderdateFrom')
        productorderdateTo = self.request.GET.get('productorderdateTo')

        if query:
            queryset = queryset.filter(
                 Q(ProductOrderSlipDiv__contains=query) | Q(ProductOrderOrderNumber__contains=query) | Q(ProductOrderBrandName__contains=query) | 
                 Q(ProductOrderDestinationCode__CustomerOmitName__icontains=query) | Q(ProductOrderShippingCode__CustomerOmitName__icontains=query) 
            )

        if productorderdateFrom and productorderdateTo:
            queryset = queryset.filter(Q(ProductOrderOrderingDate__range=(productorderdateFrom,productorderdateTo)))

        return queryset

# 受発注情報登録
class ProductOrderCreateView(LoginRequiredMixin,CreateView):
    model = ProductOrder
    form_class =  ProductOrderForm
    template_name = "crud/productorder/new/productorderform.html"
   
    def get(self, request):
        form = ProductOrderForm(self.request.POST or None)

        context = {
            'form': form,
        }

        return render(request, 'crud/productorder/new/productorderform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST': 
            
            if form.is_valid():
                post.ProductOrderOrderNumber = post.ProductOrderOrderNumber.zfill(7)
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                post.save()      
        else:
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form))

        return redirect('myapp:productorderlist')  

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))