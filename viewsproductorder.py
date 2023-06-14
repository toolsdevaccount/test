from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import ProductOrder, MerchandiseColor, MerchandiseSize
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q
# 日時
#from django.utils import timezone
#import datetime
# forms
from .formsproductorder import ProductOrderForm, ProductOrderFormset
# Transaction
from django.db import transaction

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
    formset_class = ProductOrderFormset
    template_name = "crud/productorder/new/productorderform.html" 
   
    def get(self, request):
        form = ProductOrderForm(self.request.POST or None)
        formset = ProductOrderFormset(self.request.POST or None)
        detailsize = MerchandiseSize.objects.filter(McdSizeId_id=1).values('id','McdSizeId_id','McdSize')
        detailcolor = MerchandiseColor.objects.filter(McdColorId_id=1).values('id','McdColorId_id','McdColor')      
        #extranum = len(detailsize) * len(detailcolor)


        context = {
            'form': form,
            'formset': formset,
            'detailsize': detailsize,
            'detailcolor':detailcolor,
        }

        return render(request, 'crud/productorder/new/productorderform.html', context)

    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = ProductOrderFormset(self.request.POST,instance=post) 

        if self.request.method == 'POST' and formset.is_valid():
            instances = formset.save(commit=False)
           
            if form.is_valid():
                post.ProductOrderOrderNumber = post.ProductOrderOrderNumber.zfill(7)
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                post.save()      

                # 明細のfileを取り出して更新
                i = 0
                for file in instances:
                    file.PodColorId_id = self.request.POST.getlist('PodDetailId-0-PodColorId')[i]
                    file.PodSizeId_id = self.request.POST.getlist('PodDetailId-0-PodSizeId')[0]
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()
                    i = i + 1
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))
        return redirect('myapp:productorderlist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))