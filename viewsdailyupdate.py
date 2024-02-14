from django.shortcuts import render,redirect
from django.views.generic import CreateView
from .models import InvoiceNo
from .formsdailyupdate import DailyUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Transaction
from django.db import transaction
# 日時
from django.utils import timezone
import datetime
# MySQL
import MySQLdb
# メッセージ
from django.contrib import messages
# 計算用
from decimal import Decimal
# LOG出力設定
import logging
logger = logging.getLogger(__name__)

class DailyUpdateView(LoginRequiredMixin,CreateView):
    model = InvoiceNo
    form_class =  DailyUpdateForm
    template_name = "crud/dailyupdate/dailyupdate.html"

    def form_valid(self, form):
        if self.request.method == "POST":
            if form.is_valid():
                try:       
                    DailyDate = form.data.get('DailyUpdateDate') 
                    dt = extract(DailyDate)
                    length=len(dt)
                    invdt = getInvoiceNo()
                    InvoiceNo = invdt[0][0]
                    #SInvoiceNo = invdt[0][1]
                    userid = self.request.user.id
                    for i in range(length):
                        InvoiceNo += Decimal(1)
                        #SInvoiceNo += Decimal(1)
                        updid = dt[i][0]
                        UpdateRequestResult(updid,DailyDate,InvoiceNo,userid)
                        UpdateInvoiceNo(InvoiceNo,userid)
                except Exception as e:
                    message = "日次更新時にエラーが発生しました"
                    logger.error(message)
                    messages.add_message(self.request, messages.ERROR, message)

                    return redirect("myapp:DailyUpdate")

            return redirect('myapp:DailyUpdate')

def extract(DailyDate):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)

    cur = conn.cursor()
    sql = (
            ' select '
            '	 c.id '
            '	,c.InvoiceIssueDiv '
            '	,c.DailyUpdateDiv '
            '	,c.DailyUpdateDate '
            ' from '
            '	myapp_orderingtable a '
            '	inner join '
            '	myapp_orderingdetail b on '
            '		a.id = b.OrderingTableId_id '
            '	inner join '
            '	myapp_RequestResult c on '
            '			 a.id = OrderingId_id '
            '		and b.id = OrderingDetailId_id '
            ' where '
            '	  a.SlipDiv IN("A","R","P","T","M","I","E","D","B","Y","Z") '
            ' and c.DailyUpdateDiv = false '
            ' and c.DailyUpdateDate <= ' + "'" + str(DailyDate) + "'"
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()
    return result

def getInvoiceNo():
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)

    cur = conn.cursor()
    sql = (
            ' select '
            '	 InvoiceNo '
            '	,SInvoiceNo '
            ' from '
            '	myapp_InvoiceNo '
            ' where '
            '	id = 1 '
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()
    return result

def UpdateRequestResult(pk,DailyUpdate,InvoiceNo,userid):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)

    cur = conn.cursor()
    sql = (
            ' update ' 
            '	myapp_requestresult '
            ' set '
            '	 InvoiceNUmber = ' + "'" + str(InvoiceNo) + "'" 
            '	,DailyUpdateDiv = true '
            '	,DailyUpdateDate = ' + "'" + str(DailyUpdate) + "'"
            '   ,Updated_id = ' + str(userid) +
            '   ,Updated_at = now() ' 
            ' where '
            '	id = ' + str(pk)
        )
    cur.execute(sql)
    result = conn.affected_rows()
    conn.commit()

    cur.close()
    conn.close()

    return result

def UpdateInvoiceNo(InvoiceNo,userid):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)

    cur = conn.cursor()
    sql = (
            ' update ' 
            '	myapp_InvoiceNo '
            ' set '
            '	 InvoiceNo  = ' + "'" + str(InvoiceNo) + "'" 
            '   ,Updated_id = ' + str(userid) +
            '   ,Updated_at = now() ' 
            ' where '
            '	id = 1'
        )
    cur.execute(sql)
    result = conn.affected_rows()
    conn.commit()

    cur.close()
    conn.close()

    return result


# 日次更新
#class DailyUpdateView(LoginRequiredMixin,CreateView):
#    model = InvoiceNo
#    form_class =  DailyUpdateForm
#    template_name = "crud/dailyupdate/dailyupdate.html"

    # get_context_dataをオーバーライド
#    def get_context_data(self, **kwargs):
#        context = super(DailyUpdateView, self).get_context_data(**kwargs)
#        return context

    # form_valid関数をオーバーライドすることで、更新するフィールドと値を指定できる
#    @transaction.atomic # トランザクション設定
#    def form_valid(self, form):
#        if self.request.method == "POST":
#            if form.is_valid():
#                post = form.save(commit=False)
                # Updatedidフィールドはログインしているユーザidとする
#                post.Updated_id = self.request.user.id
#                post.Updated_at = timezone.now() + datetime.timedelta(hours=9) # 現在の日時
#                post.save()
#            return redirect('myapp:DailyUpdate')

    # バリデーションエラー時
#    def form_invalid(self, form):
#        return super().form_invalid(form) 