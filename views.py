from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView, UpdateView
from .models import CustomerSupplier
from .forms import CustomerSupplierForm,SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q

# reportLab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
import os

# fileupload
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# 日時
from django.utils import timezone
import datetime

# signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# index
def index(request):
    return render(request, 'crud/index.html', {})

# PDF出力
def pdftest(request):
    if request.method == 'POST':
        # ユーザのデスクトップのディレクトリを取得
        file = "sample.pdf"
        file_path = os.path.expanduser("~") + "/Desktop/" + file

        # A4の新規PDFファイルを作成
        page = canvas.Canvas(file_path, pagesize=portrait(A4))
        
        # 指定座標が中心となるように文字を挿入
        page.drawCentredString(200, 200, "Hello World!")

        # PDFファイルとして保存
        page.save() 
        
    return render(request, 'crud/pdftest/pdftest.html', {})

# fileupload
def uploadtest(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'crud/upload/uploadtest.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'crud/upload/uploadtest.html')

# 得意先仕入先マスター一覧/検索
class CustomerSupplierListView(LoginRequiredMixin,ListView):
    model = CustomerSupplier
    context_object_name = 'object_list'
    queryset = CustomerSupplier.objects.order_by('CustomerCode')
    template_name = "crud/customersupplier/customersupplierlist.html"
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
    template_name = "crud/customersupplier/customersupplierform.html"

    def get(self, request):
        form = CustomerSupplierForm
        context = {
            'form': form,
        }
        return render(request, 'crud/customersupplier/customersupplierform.html', context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        post = form.save(commit=False)
        # Createid,Updatedidフィールドはログインしているユーザidとする
        post.Created_id = self.request.user.id
        post.Updated_id = self.request.user.id
        post.Created_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
        post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
        post.save()

        return redirect('myapp:list')
    # バリデーションエラー時
    def form_invalid(self, form):
        #a = self.request.user
        return super().form_invalid(form)

# 得意先仕入先マスター更新
class CustomerSupplierUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomerSupplier
    form_class =  CustomerSupplierForm
    template_name = "crud/customersupplier/customersupplierupdateform.html"
       
    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        if self.request.method == "POST":
            post = form.save(commit=False)
            # Updatedidフィールドはログインしているユーザidとする
            post.Updated_id = self.request.user.id
            post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
            post.save()
        return redirect('myapp:list')

    # バリデーションエラー時
    def form_invalid(self, form):
        #a = self.request.user
        return super().form_invalid(form) 

# 得意先仕入先マスター削除
class CustomerSupplierDeleteView(LoginRequiredMixin,UpdateView):
    model = CustomerSupplier
    form_class =  CustomerSupplierForm
    template_name = "crud/customersupplier/customersupplierdeleteform.html"
       
    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    def form_valid(self, form):
        if self.request.method == "POST":
            post = form.save(commit=False)
            # 
            post.is_Deleted = True
            post.save()

        return redirect('myapp:list')
