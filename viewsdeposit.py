from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import Deposit,CustomerSupplier
from .formsdeposit import DepositForm, DepositSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
# 検索機能のために追加
from django.db.models import Q
# Transaction
from django.db import transaction
# 日時
from django.utils import timezone
import datetime

# 入金情報一覧/検索
class DepositListView(LoginRequiredMixin,ListView):
    model = Deposit
    context_object_name = 'object_list'
    queryset = Deposit.objects.order_by('id').reverse()
    template_name = "crud/deposit/list/depositlist.html"
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        search = [
            self.request.POST.get('query', None),
        ]
        request.session['dpsearch'] = search
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    #検索機能
    def get_queryset(self):
        if 'dpsearch' in self.request.session:
            search = self.request.session['dpsearch']
            query = search[0]
        else:
            query = self.request.POST.get('query', None)

        # コード順
        queryset = Deposit.objects.order_by('id').reverse()
        # 削除済除外
        queryset = queryset.filter(is_Deleted=0)

        if query:
            queryset = queryset.filter(
                 Q(DepositCustomerCode__CustomerOmitName__icontains=query) | Q(DepositMoney__contains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        query = ''
        if 'dpsearch' in self.request.session:
            search = self.request.session['dpsearch']
            query = search[0]

        default_data = {'query': query }
        
        form = DepositSearchForm(initial=default_data) # 検索フォーム
        context['dpsearch'] = form
        return context
       
# 入金情報登録
class DepositCreateView(LoginRequiredMixin,CreateView):
    model = Deposit
    form_class =  DepositForm
    template_name = "crud/deposit/new/depositform.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(DepositCreateView, self).get_context_data(**kwargs)
        context.update(DepositCustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),)
        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':            
            if form.is_valid():
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                post.Created_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                post.save()       
        else:
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form))
        return redirect('myapp:Depositlist')
    # バリデーションエラー時
    def form_invalid(self, form):
        return super().form_invalid(form)

# 入金情報更新
class DepositUpdateView(LoginRequiredMixin,UpdateView):
    model = Deposit
    form_class =  DepositForm
    template_name = "crud/deposit/update/depositformupdate.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(DepositUpdateView, self).get_context_data(**kwargs)
        context.update(DepositCustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),)
        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        if self.request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                # Updatedidフィールドはログインしているユーザidとする
                post.Updated_id = self.request.user.id
                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                post.save()
            return redirect('myapp:Depositlist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return super().form_invalid(form) 

# 入金情報削除
class DepositDeleteView(LoginRequiredMixin,UpdateView):
    model = Deposit
    form_class =  DepositForm
    template_name = "crud/deposit/delete/depositformdelete.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(DepositDeleteView, self).get_context_data(**kwargs)
        context.update(DepositCustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),)
        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        if self.request.method == "POST":
            post = form.save(commit=False)
 
            post.Updated_id = self.request.user.id
            post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
            post.is_Deleted = True
            post.save()

        return redirect('myapp:Depositlist')
