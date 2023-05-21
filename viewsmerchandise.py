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
from .formsmerchandise import MerchandiseForm, MerchandiseFormset, MerchandiseColorFormset, MerchandiseSizeFormset, MerchandisefileFormset
# Transaction
from django.db import transaction
# fileupload
from django.conf import settings
from django.core.files.storage import FileSystemStorage

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
        # 商品コード大きい順で抽出
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
    formset_class = MerchandiseFormset
    inlinescolor_class = MerchandiseColorFormset
    inlinesize_class = MerchandiseSizeFormset
    inlinefile_class = MerchandisefileFormset
    template_name = "crud/merchandise/merchandiseform.html"
   
    def get(self, request):
        form = MerchandiseForm(self.request.POST or None)
        formset = MerchandiseFormset
        inlinescolor = MerchandiseColorFormset
        inlinessize = MerchandiseSizeFormset
        inlinesfile = MerchandisefileFormset

        context = {
            'form': form,
            'formset': formset,
            'inlinescolor': inlinescolor,
            'inlinessize': inlinessize,
            'inlinesfile': inlinesfile,
        }


        return render(request, 'crud/merchandise/merchandiseform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = MerchandiseFormset(self.request.POST,instance=post) 
        inlinescolor = MerchandiseColorFormset(self.request.POST,instance=post)
        inlinessize = MerchandiseSizeFormset(self.request.POST,instance=post)
        inlinesfile = MerchandisefileFormset(self.request.POST,self.request.FILES,instance=post)

        if self.request.method == 'POST' and formset.is_valid() and inlinescolor.is_valid() and inlinessize.is_valid() and inlinesfile.is_valid(): 
            instances = formset.save(commit=False)
            instancecolor = inlinescolor.save(commit=False)
            instancesize = inlinessize.save(commit=False)
            instancefile = inlinesfile.save(commit=False)
            
            if form.is_valid():
                # Created_id,Updated_idフィールドはログインしているユーザidとする
                post.Created_id = self.request.user.id
                post.Updated_id = self.request.user.id
                post.save()
        
                for file in instances:
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()

                for file in instancecolor:
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()

                for file in instancesize:
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()

                for file in instancefile:
                    #myfile = self.request.FILES['ProductOrderupload']
                    #fs = FileSystemStorage()
                    #filename = fs.save(myfile.name, myfile)
                    #uploaded_file_url = fs.url(filename)
                    file.Created_id = self.request.user.id
                    file.Updated_id = self.request.user.id
                    file.save()

        else:
            print(inlinesfile.non_form_errors)
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form, formset=formset, inlinescolor=inlinescolor, inlinessize=inlinessize, inlinesfile=inlinesfile,))
 
        return redirect('myapp:merchandiselist')

    # バリデーションエラー時
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class, inlinescolor=self.inlinescolor_class, inlinessize=self.inlinesize_class, inlinesfile=self.inlinefile_class))
