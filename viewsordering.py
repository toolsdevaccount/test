from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import OrderingTable, OrderingDetail, CustomerSupplier
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q
# 日時
from django.utils import timezone
import datetime
from datetime import date
# forms
from .forms import OrderingForm,OrderingFormset
# Transaction
from django.db import transaction

# 受発注一覧/検索
class OrderingListView(LoginRequiredMixin,ListView):
    model = OrderingTable
    form_class = OrderingForm
    context_object_name = 'object_list'
    queryset = OrderingTable.objects.order_by('OrderingDate','Created_at').reverse()
    template_name = "crud/ordering/list/orderinglist.html"
    paginate_by = 10

    #検索機能
    def get_queryset(self):
        # 依頼日、伝票区分、オーダーNO大きい順で抽出
        queryset = OrderingTable.objects.order_by('OrderingDate','SlipDiv','OrderNumber').reverse()
        # 削除済以外、管理者の場合は全レコード表示（削除済以外）
        if self.request.user.is_superuser == 0:
            queryset = queryset.filter(is_Deleted=0,Created_id=self.request.user.id)
        else:
            queryset = queryset.filter(is_Deleted=0)

        query = self.request.GET.get('query')      
        orderdateFrom = self.request.GET.get('orderdateFrom')
        orderdateTo = self.request.GET.get('orderdateTo')

        if query:
            queryset = queryset.filter(
                 Q(SlipDiv__contains=query) | Q(OrderNumber__contains=query) | Q(ProductName__contains=query) | Q(MarkName__contains=query) |
                 Q(DestinationCode__CustomerOmitName__icontains=query) | Q(ShippingCode__CustomerOmitName__icontains=query) 
            )

        if orderdateFrom and orderdateTo:
            queryset = queryset.filter(Q(OrderingDate__range=(orderdateFrom,orderdateTo)))

        return queryset

# 受発注情報登録
class OrderingCreateView(LoginRequiredMixin,CreateView):
    model = OrderingTable
    form_class =  OrderingForm
    formset_class = OrderingFormset
    template_name = "crud/ordering/new/orderingform.html"
   
    def get(self, request):
        form = OrderingForm(self.request.POST or None, 
                            initial={'OutputDiv': '1',
                                     'OrderingDate':date.today(),
                                     })
        formset = OrderingFormset
        DestinationCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode')
        SupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=3) | Q(MasterDiv=4)).order_by('CustomerCode')
        ShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode')
        CustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=2) | Q(MasterDiv=4)).order_by('CustomerCode')
        RequestCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode')
        StainShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode')
        
        context = {
            'form': form,
            'formset': formset,
            'DestinationCode': DestinationCode,
            'SupplierCode':SupplierCode,
            'ShippingCode':ShippingCode,
            'CustomerCode':CustomerCode,
            'RequestCode':RequestCode,
            'StainShippingCode':StainShippingCode,
        }

        return render(request, 'crud/ordering/new/orderingform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = OrderingFormset(self.request.POST,instance=post) 
        if self.request.method == 'POST' and formset.is_valid(): 
            instances = formset.save(commit=False)
            
            if form.is_valid():
                post.OrderNumber = post.OrderNumber.zfill(7)
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                post.save()
        
                for file in instances:
                    file.DetailItemNumber = file.DetailItemNumber.zfill(4)
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()
        else:
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

        return redirect('myapp:orderinglist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))

# 受発注情報編集
class orderingUpdateView(LoginRequiredMixin,UpdateView):
    model = OrderingTable
    form_class =  OrderingForm
    formset_class = OrderingFormset
    template_name = "crud/ordering/update/orderingformupdate.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(orderingUpdateView, self).get_context_data(**kwargs)
        context.update(dict(formset=OrderingFormset(self.request.POST or None, instance=self.get_object(), queryset=OrderingDetail.objects.filter(is_Deleted=0))),
                       DestinationCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode'),
                       SupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=3) | Q(MasterDiv=4)).order_by('CustomerCode'),
                       ShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode'),
                       CustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=2) | Q(MasterDiv=4)).order_by('CustomerCode'),
                       RequestCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode'),
                       StainShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode'),
                       )
        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = OrderingFormset(self.request.POST,instance=post) 

        if self.request.method == 'POST' and formset.is_valid(): 
            instances = formset.save(commit=False)
           
            if form.is_valid():
                post.OrderNumber = post.OrderNumber.zfill(7)
                # Updated_idフィールドはログインしているユーザidとする
                post.Updated_id = self.request.user.id
                # Updated_atは現在日付時刻とする
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時               
                post.save()

                # 削除チェックがついたfileを取り出して更新
                for file in formset.deleted_objects:
                    file.Updated_id = self.request.user.id
                    file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                    file.is_Deleted = True
                    file.save()

                # 明細のfileを取り出して更新
                for file in instances:
                    file.DetailItemNumber = file.DetailItemNumber.zfill(4)
                    file.Updated_id = self.request.user.id
                    file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                    file.save()
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class)) 
        return redirect('myapp:orderinglist')

    # バリデーションエラー時
    def form_invalid(self,form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))

# 受発注情報削除
class orderingDeleteView(LoginRequiredMixin,UpdateView):
    model = OrderingTable
    form_class =  OrderingForm
    formset_class = OrderingFormset
    template_name = "crud/ordering/delete/orderingformdelete.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(orderingDeleteView, self).get_context_data(**kwargs)
        context.update(dict(formset=OrderingFormset(self.request.POST or None, instance=self.get_object(), queryset=OrderingDetail.objects.filter(is_Deleted=0))))
        
        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = OrderingFormset(self.request.POST,instance=post) 

        if self.request.method == 'POST':           
            if form.is_valid():
                post.is_Deleted = True
                # Updated_idフィールドはログインしているユーザidとする
                post.Updated_id = self.request.user.id
                # Updated_atは現在日付時刻とする
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時               
                post.save()

            if formset.is_valid():
                instances = formset.save(commit=False)
                # 明細のfileを取り出して削除
                for file in instances:
                    file.is_Deleted = True
                    file.Updated_id = self.request.user.id
                    file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                    file.save()
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))        
        return redirect('myapp:orderinglist')

    # バリデーションエラー時
    def form_invalid(self,form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))        