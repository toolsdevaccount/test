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

                    if length == 0:
                        message = "更新対象データがありませんでした"
                        logger.error(message)
                        messages.add_message(self.request, messages.WARNING, message)

                        return redirect("myapp:DailyUpdate")
                    userid = self.request.user.id
                    OrderNumber = ''
                    for i in range(length):
                        updid = dt[i][0]
                        SlipDiv = dt[i][4]
                        invdt = getInvoiceNo()
                        if SlipDiv == "A" or SlipDiv == "R" or SlipDiv == "P" or SlipDiv == "T" or SlipDiv == "M" or SlipDiv == "I" or SlipDiv == "E" or SlipDiv == "D" or SlipDiv == "B" or SlipDiv == "Y" or SlipDiv ==  "Z":
                            InvoiceNo = invdt[0][0]
                        else:
                            InvoiceNo = invdt[0][1]

                        if OrderNumber != str(dt[i][4] + dt[i][5]):
                            InvoiceNo += Decimal(1)

                        UpdateRequestResult(updid,DailyDate,InvoiceNo,userid)
                        UpdateInvoiceNo(InvoiceNo,userid,SlipDiv)
                        OrderNumber = str(dt[i][4] + dt[i][5])
                except Exception as e:
                    message = "日次更新時にエラーが発生しました"
                    logger.error(message)
                    messages.add_message(self.request, messages.ERROR, message)

                    return redirect("myapp:DailyUpdate")

            message = "日次更新処理正常終了"
            logger.error(message)
            messages.add_message(self.request, messages.SUCCESS, message)

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
            '   ,a.SlipDiv'
            '   ,a.OrderNumber'
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
            '     c.DailyUpdateDiv = false '
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

def UpdateInvoiceNo(InvoiceNo,userid,SlipDiv):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)

    cur = conn.cursor()
    if SlipDiv == "A" or SlipDiv == "R" or SlipDiv == "P" or SlipDiv == "T" or SlipDiv == "M" or SlipDiv == "I" or SlipDiv == "E" or SlipDiv == "D" or SlipDiv == "B" or SlipDiv == "Y" or SlipDiv ==  "Z":
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
    else:
        sql = (
                ' update ' 
                '	myapp_InvoiceNo '
                ' set '
                '	 SInvoiceNo  = ' + "'" + str(InvoiceNo) + "'" 
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