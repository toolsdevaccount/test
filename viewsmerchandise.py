from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView
from .models import Merchandise
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q
# 日時
from django.utils import timezone
import datetime
# forms
from .formsmerchandise import MerchandiseForm
# Transaction
from django.db import transaction

# 商品一覧/検索
class MerchandiseListView(LoginRequiredMixin,ListView):
    model = Merchandise
    form_class = MerchandiseForm
    context_object_name = 'object_list'
    queryset = Merchandise.objects.order_by('McdCode','Created_at').reverse()
    template_name = "crud/merchandise/merchandiselist.html"
    paginate_by = 10

    #検索機能
    def get_queryset(self):
        # 依頼日大きい順で抽出
        queryset = Merchandise.objects.order_by('McdCode','Created_at').reverse()
        # 削除済除外
        queryset = queryset.filter(is_Deleted=0)
        query = self.request.GET.get('query')      

        if query:
            queryset = queryset.filter(
                 Q(McdCode__contains=query) | Q(McdPartNumber__contains=query) | Q(McdManagerCode__first_name__icontains=query)  
            )

        return queryset

# 商品情報登録
class MerchandiseCreateView(LoginRequiredMixin,CreateView):
    model = Merchandise
    form_class =  MerchandiseForm
    template_name = "crud/merchandise/merchandiseform.html"
   
    def get(self, request):
        form = MerchandiseForm(self.request.POST or None)

        context = {
            'form': form,
        }

        return render(request, 'crud/merchandise/merchandiseform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST': 
            
            if form.is_valid():
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                post.save()      
        else:
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form))

        return redirect('myapp:merchandiselist')  

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))  
