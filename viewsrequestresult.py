from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import OrderingTable, OrderingDetail, CustomerSupplier, RequestResult
from django.contrib.auth.mixins import LoginRequiredMixin

# 検索機能のために追加
from django.db.models import Q
# 日時
from django.utils import timezone
import datetime
from datetime import date

# forms
from .formsrequestresult import RequestResultForm, RequestRecordFormset, RequestResultFormset, SearchForm
# Transaction
from django.db import transaction
# SQL直接実行
from django.db import connection
# ajax
from django.http import JsonResponse

# 受発注一覧/検索
class RequestResultListView(LoginRequiredMixin,ListView):
    model = OrderingTable
    form_class = RequestResultForm
    context_object_name = 'object_list'
    queryset = OrderingDetail.objects.select_related()
    template_name = "crud/requestresult/list/requestresultlist.html"
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        search = [
            self.request.POST.get('query', None),
            self.request.POST.get('key', None),
            self.request.POST.get('word', None),
            self.request.POST.get('orderdateFrom', None),
            self.request.POST.get('orderdateTo', None),
        ]
        request.session['rqsearch'] = search
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    #検索機能
    def get_queryset(self):
        if 'rqsearch' in self.request.session:
            search = self.request.session['rqsearch']
            query = search[0]
            key = search[1]
            word = search[2]
            orderdateFrom = search[3]
            orderdateTo = search[4]
        else:
            query = self.request.POST.get('query', None)
            key = self.request.POST.get('key', None)
            word = self.request.POST.get('word', None)
            orderdateFrom = self.request.POST.get('orderdateFrom', None)
            orderdateTo = self.request.POST.get('orderdateTo', None)

        # 依頼日、伝票区分、オーダーNO大きい順で抽出
        queryset = OrderingTable.objects.order_by('OrderingDate','SlipDiv','OrderNumber').reverse()
        # 削除済以外、管理者の場合は全レコード表示（削除済以外）
        if self.request.user.is_superuser == 0:
            #queryset = queryset.filter(is_Deleted=0,Created_id=self.request.user.id)
            # 全ユーザ表示
            queryset = queryset.filter(is_Deleted=0)
        else:
            queryset = queryset.filter(is_Deleted=0)

        if query:
            queryset = queryset.filter(
                 Q(SlipDiv__contains=query) | Q(OrderNumber__contains=query) | Q(ProductName__contains=query) | Q(MarkName__contains=query) |
                 Q(DestinationCode__CustomerOmitName__icontains=query) | Q(ShippingCode__CustomerOmitName__icontains=query) | 
                 Q(SampleDiv__divname__icontains=query) | Q(RequestCode__CustomerOmitName__icontains=query) |
                 Q(OutputDiv__outputdivname__icontains=query) 
            )
        if key:
            queryset = queryset.filter(
                 Q(SlipDiv__contains=key) | Q(OrderNumber__contains=key) | Q(ProductName__contains=key) | Q(MarkName__contains=key) |
                 Q(DestinationCode__CustomerOmitName__icontains=key) | Q(ShippingCode__CustomerOmitName__icontains=key) |
                 Q(SampleDiv__divname__icontains=key) | Q(RequestCode__CustomerOmitName__icontains=key) |
                 Q(OutputDiv__outputdivname__icontains=key) 
            )

        if word:
            queryset = queryset.filter(
                 Q(SlipDiv__contains=word) | Q(OrderNumber__contains=word) | Q(ProductName__contains=word) | Q(MarkName__contains=word) |
                 Q(DestinationCode__CustomerOmitName__icontains=word) | Q(ShippingCode__CustomerOmitName__icontains=word) | 
                 Q(SampleDiv__divname__icontains=word) | Q(RequestCode__CustomerOmitName__icontains=word) |
                 Q(OutputDiv__outputdivname__icontains=word) 
            )

        if orderdateFrom and orderdateTo:
            queryset = queryset.filter(Q(OrderingDate__range=(orderdateFrom,orderdateTo)))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        query = ''
        key = ''
        word = ''
        orderdateFrom = ''
        orderdateTo = ''
        if 'rqsearch' in self.request.session:
            search = self.request.session['rqsearch']
            query = search[0]
            key = search[1]
            word = search[2]
            orderdateFrom = search[3]
            orderdateTo = search[4]

        default_data = {'query': query,
                        'key': key,
                        'word': word,
                        'orderdateFrom': orderdateFrom,
                        'orderdateTo': orderdateTo,
                       }
        
        form = SearchForm(initial=default_data) # 検索フォーム
        context['rqsearch'] = form
        return context

# 受発注情報登録
class RequestResultCreateView(LoginRequiredMixin,UpdateView):
    model = OrderingTable
    form_class =  RequestResultForm
    formset_class = RequestResultFormset
    inlinesRecord_class = RequestRecordFormset
    template_name = "crud/requestresult/new/requestresultform.html"
  
    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(RequestResultCreateView, self).get_context_data(**kwargs)
        context.update(dict(formset=RequestResultFormset(self.request.POST or None, instance=self.get_object(), queryset=OrderingDetail.objects.filter(is_Deleted=0))),
                       inlinesRecord=RequestRecordFormset(self.request.POST or None),
                       DestinationCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       SupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=3) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode'),
                       ShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       CustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=2) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode'),
                       RequestCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       StainShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       ) 
        return context

    def exec_ajax(request):
        if request.method == 'GET':  # GETの処理
            param = request.GET.get("param")  # GETパラメータ
            #
            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            # 取得するSQL
            with connection.cursor() as cursor:
                cursor.execute(
                                " select "
                                    " id                    AS id, "
                                    " DetailItemNumber      AS ResultItemNumber, "
                                    " SpecifyDeliveryDate   AS ResultDate, "
                                    " StainAnswerDeadline   AS ShippingDate "
                                " from " 
                                    " myapp_orderingdetail "
                                " where "
                                "     id = %s "
                            , [str(param)])
                detail = dictfetchall(cursor)

            context = {
                'list': detail,
            }

            return JsonResponse(context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        #formset = RequestResultFormset(self.request.POST,instance=post) 
        inlinesRecord = RequestRecordFormset(self.request.POST,instance=post)

        if self.request.method == 'POST' and inlinesRecord.is_valid():
            if inlinesRecord.is_valid():
                instances = inlinesRecord.save(commit=False)
                # 明細のfileを取り出して更新
                for file in instances:
                    if not file.OrderingDetailId_id is None:
                        file.Created_id = self.request.user.id
                        file.Updated_id = self.request.user.id
                        file.Created_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                        file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時

                        file.save()
        else:
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class)) 
        return redirect('myapp:requestresultlist')

    # バリデーションエラー時
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["formset"] = RequestResultFormset(self.request.POST or None, instance=self.get_object(), queryset=OrderingDetail.objects.filter(is_Deleted=0)),
        context["DestinationCode"] = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0)
        context["SupplierCode"] = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=3) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode')
        context["ShippingCode"] = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0)
        context["CustomerCode"] = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=2) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode')
        context["RequestCode"] = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0)
        context["StainShippingCode"] = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0)

        return self.render_to_response(context)
        #return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))

# 受発注情報編集
class RequestResultUpdateView(LoginRequiredMixin,UpdateView):
    model = OrderingTable
    form_class =  RequestResultForm
    formset_class = RequestResultFormset
    template_name = "crud/requestresult/update/requestresultformupdate.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        queryset = RequestResult.objects.filter(is_Deleted=0, OrderingId_id=pk)       
        abc = queryset.values_list("OrderingDetailId_id",flat=True).first()

        context = super(RequestResultUpdateView, self).get_context_data(**kwargs)
        context.update(dict(formset=RequestResultFormset(self.request.POST or None, instance=self.get_object(), queryset=OrderingDetail.objects.filter(is_Deleted=0))),
                       inlinesRecord=RequestRecordFormset(self.request.POST or None, instance=self.get_object(), queryset=RequestResult.objects.filter(is_Deleted=0, OrderingDetailId_id=abc)),
                       DestinationCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       SupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=3) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode'),
                       ShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       CustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=2) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode'),
                       RequestCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       StainShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       )
        return context

    def exec_ajax_result(request):
        if request.method == 'GET':  # GETの処理
            param = request.GET.get("param")  # GETパラメータ
            #
            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            # 取得するSQL
            with connection.cursor() as cursor:
                cursor.execute(
                                " select "
                                    " id                    AS id, "
                                    " ResultItemNumber      AS ResultItemNumber, "
                                    " ResultDate            AS ResultDate, "
                                    " ShippingDate          AS ShippingDate, "
                                    " ShippingVolume        AS ShippingVolume, "
                                    " SlipNumber            AS SlipNumber, "
                                    " ResultSummary         AS ResultSummary, "
                                    " ResultMoveDiv         AS ResultMoveDiv, "
                                    " ResultGainDiv         AS ResultGainDiv, "
                                    " ResultDecreaseDiv     AS ResultDecreaseDiv, "
                                    " OrderingDetailId_id   AS OrderingDetailId_id "
                                " from " 
                                    " myapp_requestresult "
                                " where "
                                "     OrderingDetailId_id = %s "
                            , [str(param)])
                detail = dictfetchall(cursor)

            context = {
                'list': detail,
            }

            return JsonResponse(context)

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        #formset = RequestResultFormset(self.request.POST,instance=post) 
        inlinesRecord = RequestRecordFormset(self.request.POST,instance=post)

        if self.request.method == 'POST' and inlinesRecord.is_valid():
            if inlinesRecord.is_valid():
                instances = inlinesRecord.save(commit=False)
                # 明細のfileを取り出して更新
                for file in instances:
                    file.Updated_id = self.request.user.id
                    file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
                    file.save()
        else:
            # is_validがFalseの場合はエラー文を表示
            return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class)) 
        return redirect('myapp:requestresultlist')

        #if self.request.method == 'POST' and formset.is_valid(): 
        #    instances = formset.save(commit=False)
           
        #    if form.is_valid():
        #        post.OrderNumber = post.OrderNumber.zfill(7)
        #        # Updated_idフィールドはログインしているユーザidとする
        #        post.Updated_id = self.request.user.id
        #        # Updated_atは現在日付時刻とする
        #        post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時               
        #        post.save()

                # 削除チェックがついたfileを取り出して更新
        #        for file in formset.deleted_objects:
        #            file.Updated_id = self.request.user.id
        #            file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
        #            file.is_Deleted = True
        #            file.save()

                # 明細のfileを取り出して更新
        #        for file in instances:
        #            file.DetailItemNumber = file.DetailItemNumber.zfill(4)
        #            file.Updated_id = self.request.user.id
        #            file.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
        #            file.save()
        #else:
        #    return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class)) 
        #return redirect('myapp:requestresultlist')

    # バリデーションエラー時
    def form_invalid(self,form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class)) 

# 受発注情報削除
class RequestResultDeleteView(LoginRequiredMixin,UpdateView):
    model = OrderingTable
    form_class =  RequestResultForm
    formset_class = RequestResultFormset
    template_name = "crud/requestresult/delete/requestresultformdelete.html"

    # get_context_dataをオーバーライド
    def get_context_data(self, **kwargs):
        context = super(RequestResultDeleteView, self).get_context_data(**kwargs)
        context.update(dict(formset=RequestResultFormset(self.request.POST or None, instance=self.get_object(), queryset=OrderingDetail.objects.filter(is_Deleted=0))),
                       DestinationCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       SupplierCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=3) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode'),
                       ShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       CustomerCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').filter(Q(MasterDiv=2) | Q(MasterDiv=4),is_Deleted=0).order_by('CustomerCode'),
                       RequestCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       StainShippingCode = CustomerSupplier.objects.values('id','CustomerCode','CustomerOmitName').order_by('CustomerCode').filter(is_Deleted=0),
                       )
        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
    @transaction.atomic # トランザクション設定
    def form_valid(self, form):
        post = form.save(commit=False)
        formset = RequestResultFormset(self.request.POST,instance=post) 

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
        return redirect('myapp:requestresultlist')

    # バリデーションエラー時
    def form_invalid(self,form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset_class))        