from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView, UpdateView
from .models import OrderingTable
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q

# 日時
from django.utils import timezone

# TEST
from .forms import OrderingForm,OrderingFormset

# 受発注一覧/検索
class OrderingListView(LoginRequiredMixin,ListView):
    model = OrderingTable
    form_class = OrderingForm
    context_object_name = 'object_list'
    queryset = OrderingTable.objects.order_by('OrderingDate').reverse()
    template_name = "crud/ordering/orderinglist.html"
    paginate_by = 10

    #検索機能
    def get_queryset(self):
        # 依頼日大きい順
        queryset = OrderingTable.objects.order_by('OrderingDate').reverse()
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
        form = OrderingForm(request.POST or None)
        formset = OrderingFormset()

        context = {
            'form': form,
            'formset': formset,
        }

        return render(request, 'crud/ordering/orderingform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        if self.request.method == 'POST': 
            post = form.save(commit=False)
            formset = OrderingFormset(self.request.POST,instance=post) 
            instances = formset.save(commit=False)
            
            if form.is_valid():
                post.OrderNumber = post.OrderNumber.zfill(7)
                post.StartItemNumber = post.StartItemNumber.zfill(4)
                post.EndItemNumber = post.EndItemNumber.zfill(4)
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                # Created_at,Updated_atは現在日付時刻とする
                post.Created_at = timezone.datetime.now() # 現在の日時
                post.Updated_at = timezone.datetime.now() # 現在の日時
                post.save()
               
            if formset.is_valid():                
                for file in instances:
                    file.DetailItemNumber = file.DetailItemNumber.zfill(4)
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.Created_at = timezone.datetime.now() # 現在の日時
                    file.Updated_at = timezone.datetime.now() # 現在の日時
                    file.save()        
        return redirect('myapp:orderinglist')

    # バリデーションエラー時
    def form_invalid(self, form):
        print(form.errors)
        #a = self.request.user
        return super().form_invalid(form)

