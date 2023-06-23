from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import ProductOrder, ProductOrderDetail
from django.contrib.auth.mixins import LoginRequiredMixin
# ajax
from django.http import JsonResponse
# 検索機能のために追加
from django.db.models import Q
# forms
from .formsproductorder import ProductOrderForm, ProductOrderFormset
# Transaction
from django.db import transaction
# SQL直接実行
from django.db import connection

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
    formset_class =  ProductOrderFormset
    template_name = "crud/productorder/new/productorderform.html"
   
    def get(self, request):
        form = ProductOrderForm(self.request.POST or None,
                initial={'ProductOrderDestinationCode': '1',
                         'ProductOrderSupplierCode': '1',
                         'ProductOrderShippingCode': '1',
                         'ProductOrderCustomeCode': '1',
                         'ProductOrderRequestCode': '1',
                         'ProductOrderApparelCode': '1',
                        })

        formset = ProductOrderFormset(self.request.POST or None)

        context = {
            'form': form,
            'formset': formset,
        }

        return render(request, 'crud/productorder/new/productorderform.html', context)

    
    def exec_ajax(request):
        if request.method == 'GET':  # GETの処理
            param = request.GET.get("param")  # GETパラメータ
            # カラーとサイズを取得する
            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            # カラーとサイズを取得するSQL
            with connection.cursor() as cursor:
                cursor.execute(" select "
                                    "a.Mcdcolorid_id   AS Mcdcolorid_id, "
                                    "a.McdColor        AS McdColor, "
                                    "b.mcdsize         AS McdSize, "
                                    "a.id              AS id, "
                                    "b.id              AS McdSizeid "
                                " from " 
                                    "myapp_merchandisecolor a " 
                                    "INNER JOIN "
                                    "myapp_merchandisesize b on "
                                        "a.McdColorId_id = b.McdSizeId_id "
                                " where " 
                                "     a.Mcdcolorid_id = %s "
                                " and a.is_Deleted = 0 "
                                 "order by "
                                "    a.id, "
                                "    b.id "
                            , [str(param)])
                weather_data = dictfetchall(cursor)

            context = {
                'list': weather_data,
            }

            return JsonResponse(context)

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

class ProductOrderUpdateView(LoginRequiredMixin,UpdateView):
    model = ProductOrder
    form_class =  ProductOrderForm
    formset_class =  ProductOrderFormset
    template_name = "crud/productorder/update/productorderformupdate.html" 
   
    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        context = super(ProductOrderUpdateView, self).get_context_data(**kwargs)
        context.update(dict(formset=ProductOrderFormset(self.request.POST or None, instance=self.get_object(), queryset=ProductOrderDetail.objects.filter(is_Deleted=0))))      

        print(context["formset"])
        return context
    
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