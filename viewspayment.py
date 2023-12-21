from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import Payment,CustomerSupplier
from .formspayment import PaymentForm, PaymentSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
# 検索機能のために追加
from django.db.models import Q
# Transaction
from django.db import transaction
# 日時
from django.utils import timezone
import datetime

# 支払情報一覧/検索
class PaymentListView(LoginRequiredMixin,ListView):
    model = Payment
    context_object_name = 'object_list'
    queryset = Payment.objects.order_by('id').reverse()
    template_name = "crud/payment/list/paymentlist.html"
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        search = [
            self.request.POST.get('query', None),
        ]
        request.session['pysearch'] = search
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    #検索機能
    def get_queryset(self):
        if 'pysearch' in self.request.session:
            search = self.request.session['pysearch']
            query = search[0]
        else:
            query = self.request.POST.get('query', None)

        # コード順
        queryset = Payment.objects.order_by('id').reverse()
        # 削除済除外
        queryset = queryset.filter(is_Deleted=0)

        if query:
            queryset = queryset.filter(
                 Q(PaymentSupplierCode__CustomerOmitName__icontains=query) | Q(PaymentMoney__contains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        query = ''
        if 'pysearch' in self.request.session:
            search = self.request.session['pysearch']
            query = search[0]

        default_data = {'query': query }
        
        form = PaymentSearchForm(initial=default_data) # 検索フォーム
        context['pysearch'] = form
        return context
       
# 支払情報登録
class PaymentCreateView(LoginRequiredMixin,CreateView):
    model = Payment
    form_class =  PaymentForm
    template_name = "crud/payment/new/paymentform.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(PaymentCreateView, self).get_context_data(**kwargs)
        context.update(PaymentSupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),)
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
        return redirect('myapp:Paymentlist')
    # バリデーションエラー時
    def form_invalid(self, form):
        return super().form_invalid(form)

# 支払情報更新
class PaymentUpdateView(LoginRequiredMixin,UpdateView):
    model = Payment
    form_class =  PaymentForm
    template_name = "crud/payment/update/paymentformupdate.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(PaymentUpdateView, self).get_context_data(**kwargs)
        context.update(PaymentSupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),)
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
            return redirect('myapp:Paymentlist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return super().form_invalid(form) 

# 支払情報削除
class PaymentDeleteView(LoginRequiredMixin,UpdateView):
    model = Payment
    form_class =  PaymentForm
    template_name = "crud/payment/delete/paymentformdelete.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(PaymentDeleteView, self).get_context_data(**kwargs)
        context.update(PaymentSupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),)
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

        return redirect('myapp:Paymentlist')
