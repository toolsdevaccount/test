from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import OrderingTable
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q

# 日時
from django.utils import timezone
import datetime

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
    template_name = "crud/ordering/orderinglist.html"
    paginate_by = 7

    #検索機能
    def get_queryset(self):
        # 依頼日大きい順
        queryset = OrderingTable.objects.order_by('OrderingDate','Created_at').reverse()
        # 削除済除外
        queryset = queryset.filter(is_Deleted=0)
        query = self.request.GET.get('query')      

        if query:
            queryset = queryset.filter(
                 Q(OrderingDate__contains=query) | Q(ProductName__contains=query) | Q(RequestCode__contains=query) | Q(SupplierPerson__contains=query)
            )
        return queryset

# 受発注情報登録
class OrderingCreateView(LoginRequiredMixin,CreateView):
    model = OrderingTable
    form_class =  OrderingForm
    formset_class = OrderingFormset
    template_name = "crud/ordering/orderingform.html"
   
    def get(self, request):
        form = OrderingForm(self.request.POST or None)
        formset = OrderingFormset

        context = {
            'form': form,
            'formset': formset,
        }

        return render(request, 'crud/ordering/orderingform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = OrderingFormset(self.request.POST,instance=post) 
        if self.request.method == 'POST' and formset.is_valid(): 
            instances = formset.save(commit=False)
            
            if form.is_valid(): 
                post.OrderNumber = post.OrderNumber.zfill(7)
                post.StartItemNumber = post.StartItemNumber.zfill(4)
                post.EndItemNumber = post.EndItemNumber.zfill(4)
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                # Created_at,Updated_atは現在日付時刻とする
                post.Created_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時               
                post.save()
        
                for file in instances:
                    file.DetailItemNumber = file.DetailItemNumber.zfill(4)
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.Created_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                    file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                    file.save()
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))                   
        return redirect('myapp:orderinglist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))


# 受発注情報編集
class orderingUpdateView(LoginRequiredMixin,UpdateView):
    model = OrderingTable
    form_class =  OrderingForm
    formset_class = OrderingFormset
    template_name = "crud/ordering/orderingupdateform.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(orderingUpdateView, self).get_context_data(**kwargs)
        context.update(dict(formset=OrderingFormset(self.request.POST or None, instance=self.get_object())))
     
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
                post.StartItemNumber = post.StartItemNumber.zfill(4)
                post.EndItemNumber = post.EndItemNumber.zfill(4)
                # Updated_idフィールドはログインしているユーザidとする
                post.Updated_id = self.request.user.id
                # Updated_atは現在日付時刻とする
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時               
                post.save()

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

        #print(form.errors)
        #return super().form_invalid(form)
        #context = self.get_context_data()
        #context['formset'] = OrderingFormset()

        #return self.render_to_response(context)
