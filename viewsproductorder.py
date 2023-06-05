from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import ProductOrder, ProductOrderDetail, MerchandiseColor, MerchandiseSize
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

from django.views.generic.edit import ModelFormMixin
from django.forms import formset_factory

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
class ProductOrderCreateView(LoginRequiredMixin,CreateView,ModelFormMixin):
    model = ProductOrder
    form_class =  ProductOrderForm
    formset_class = ProductOrderFormset

    template_name = "crud/productorder/new/productorderform.html"  
   
    def get(self, request):
        form = ProductOrderForm(self.request.POST or None)
        formset = ProductOrderFormset
        #detail_size = MerchandiseSize.objects.all()
        #detail_color = MerchandiseColor.objects.all()
        
        #volume = []
        #color_list = []
        #for color in detail_color:
        #    color_list.append((color))
        #    size_list = []
        #    for size in detail_size:
        #        size_list.append((size))

            # colorとsizeリストをtupleで持つ
        #    volume.append((color_list, size_list))

        #testformset = formset_factory(ProductOrderForm)
        #formset = testformset(initial=volume)

        context = {
            'form': form,
            'formset': formset,
            'detail_size': MerchandiseSize.objects.all(),
            'detail_color': MerchandiseColor.objects.all()
        }

        return render(request, 'crud/productorder/new/productorderform.html', context)


    #def get_context_data(self, **kwargs):
    #        context = super(ProductOrderCreateView, self).get_context_data(**kwargs)
    #        context.update({
    #            'formset': ProductOrderFormset(**self.get_form_kwargs()),
    #            'detail_color': MerchandiseColor.objects.all(),
    #            'detail_size': MerchandiseSize.objects.all(),
    #        })

    #        return context

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
                for file in instances:
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))
        return redirect('myapp:productorderlist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))