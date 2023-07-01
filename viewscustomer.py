from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView, UpdateView
from .models import CustomerSupplier
from .forms import CustomerSupplierForm
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q

# 日時
from django.utils import timezone
import datetime

# 得意先仕入先マスター一覧/検索
class CustomerSupplierListView(LoginRequiredMixin,ListView):
    model = CustomerSupplier
    context_object_name = 'object_list'
    queryset = CustomerSupplier.objects.order_by('CustomerCode')
    template_name = "crud/customersupplier/list/customersupplierlist.html"
    paginate_by = 10

    #検索機能
    def get_queryset(self):
        # コード順
        queryset = CustomerSupplier.objects.order_by('CustomerCode')
        # 削除済除外
        queryset = queryset.filter(is_Deleted=0)
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                 Q(CustomerName__contains=query) | Q(Municipalities__contains=query) | Q(CustomerCode__contains=query) | Q(CustomerNameKana__contains=query)
            )
        return queryset
       
# 得意先仕入先マスター登録
class CustomerSupplierCreateView(LoginRequiredMixin,CreateView):
    model = CustomerSupplier
    form_class =  CustomerSupplierForm
    template_name = "crud/customersupplier/new/customersupplierform.html"

    def get(self, request):
        form = CustomerSupplierForm(self.request.POST or None,initial=
            {
            'PrefecturesCode': '1',
            'LastClaimBalance': 0,
            'LastReceivable': 0,
            'LastPayable': 0,
            'LastProceeds': 0,
            'ProceedsTarget': 0,
            })

        context = {
            'form': form,
        }
        return render(request, 'crud/customersupplier/new/customersupplierform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        post = form.save(commit=False)
        # Createid,Updatedidフィールドはログインしているユーザidとする
        post.Created_id = self.request.user.id
        post.Updated_id = self.request.user.id
        post.save()

        return redirect('myapp:list')
    # バリデーションエラー時
    def form_invalid(self, form):
        return super().form_invalid(form)

# 得意先仕入先マスター更新
class CustomerSupplierUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomerSupplier
    form_class =  CustomerSupplierForm
    template_name = "crud/customersupplier/update/customersupplierformupdate.html"
       
    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        if self.request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                # Updatedidフィールドはログインしているユーザidとする
                post.Updated_id = self.request.user.id
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                post.save()
            return redirect('myapp:list')

    # バリデーションエラー時
    def form_invalid(self, form):
        return super().form_invalid(form) 

# 得意先仕入先マスター削除
class CustomerSupplierDeleteView(LoginRequiredMixin,UpdateView):
    model = CustomerSupplier
    form_class =  CustomerSupplierForm
    template_name = "crud/customersupplier/delete/customersupplierformdelete.html"
       
    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        if self.request.method == "POST":
            post = form.save(commit=False)
 
            post.Updated_id = self.request.user.id
            post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
            post.is_Deleted = True
            post.save()

        return redirect('myapp:list')
