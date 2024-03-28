from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait  
from reportlab.platypus import Table, TableStyle, LongTable
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from .models import Deposit, CustomerSupplier, RequestResult
# 日時
from django.utils import timezone
import datetime
from dateutil import relativedelta
# 計算用
from decimal import Decimal
from django.db.models import Sum,F,DecimalField
from django.db.models.functions import Abs
from django.db.models.functions import Coalesce
import math
from itertools import chain

# メッセージ
from django.contrib import messages
#LOG出力設定
import logging
logger = logging.getLogger(__name__)

def pdf(request, pkclosing, invoiceDate_From, invoiceDate_To, element_From, element_To):
    try:
        strtime = timezone.now() + datetime.timedelta(hours=9)
        filename = "Invoice_" + strtime.strftime('%Y%m%d%H%M%S')
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
        # 文字列を日付に変換する
        search_date = conversion(invoiceDate_From, invoiceDate_To, pkclosing)
        result = make(pkclosing, search_date[0], search_date[1], element_From, element_To, search_date[2], search_date[3],response, request)
    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        logger.error(message)
        messages.add_message(request, messages.ERROR, message)
        return redirect("myapp:invoicelist")
    if result==99:
        message = "請求書発行データがありません"
        messages.add_message(request, messages.WARNING, message)
        return redirect("myapp:invoicelist")
    return response

def make(closing, invoiceDate_From, invoiceDate_To, element_From, element_To, lastdate, billdate, response, request):
    pdf_canvas = set_info(response) # キャンバス名
    dt_own = Own_Company()
    dt_company = company(closing, element_From, element_To)
    counter = len(dt_company)
    if counter==0:
        result=99
        return result
    
    for i in range(counter):
        dt = customer(i, dt_company)
        dt_Prev = PrevBalance(lastdate, dt, invoiceDate_From, invoiceDate_To)
        dt_Detail = Detail(dt, invoiceDate_From, invoiceDate_To)

        if dt_Detail:
            print_string(pdf_canvas, dt_own, dt, billdate, dt_Prev, dt_Detail, invoiceDate_From)
            result=0

    pdf_canvas.save() # 保存
    return result

def conversion(invoiceDate_From, invoiceDate_To, pkclosing):
    # 前月同日を算出する
    if pkclosing==31:
        tdate = datetime.datetime.strptime(str(invoiceDate_From), '%Y%m%d')
        lastdate = tdate - relativedelta.relativedelta(days=1)
    else:
        tdate = datetime.datetime.strptime(str(invoiceDate_To), '%Y%m%d')
        lastdate = tdate - relativedelta.relativedelta(months=1)

    # 文字列を日付に変換する
    invoiceDate_From = datetime.datetime.strptime(str(invoiceDate_From), '%Y%m%d') 
    invoiceDate_To = datetime.datetime.strptime(str(invoiceDate_To), '%Y%m%d')

    # 日付型に変換する
    # 前月同日
    lastdate = lastdate.strftime('%Y-%m-%d')
    # 日付範囲指定From
    Date_From = invoiceDate_From.strftime('%Y-%m-%d') 
    # 日付範囲指定To
    Date_To = invoiceDate_To.strftime('%Y-%m-%d') 
    # 請求日
    billdate = invoiceDate_To.strftime('%Y年%m月%d日')
    return(Date_From, Date_To, lastdate, billdate)

#一括請求書
def set_info(response):
    pdf_canvas = canvas.Canvas(response,pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("一括請求書")
    pdf_canvas.setSubject("一括請求書")
    return pdf_canvas

def Own_Company():
    queryset = CustomerSupplier.objects.filter(CustomerCode=('A0042'))
    Own_Company = list(queryset.values(
                                    'CustomerCode',
                                    'CustomerName',
                                    'PostCode',
                                    'PrefecturesCode__prefecturename',
                                    'Municipalities',
                                    'Address',
                                    'BuildingName',
                                    'PhoneNumber',
                                    'FaxNumber',
                                ))

    return Own_Company

def company(closing, element_From, element_To):
    queryset = CustomerSupplier.objects.filter(CustomerCode__range=(element_From,element_To),ClosingDate=(closing))
    Company = list(queryset.values(
                                    'id',
                                    'CustomerCode',
                                    'CustomerName',
                                    'Department',
                                    'PostCode',
                                    'PrefecturesCode__prefecturename',
                                    'Municipalities',
                                    'Address',
                                    'BuildingName',
                                    'ClosingDate',
                                    'LastClaimBalance',
                            ))

    return Company

def customer(i, dt_company):
    queryset = CustomerSupplier.objects.filter(CustomerCode=(str(dt_company[i]['CustomerCode'])))
    Customer = list(queryset.values(
                                    'id',
                                    'CustomerCode',
                                    'CustomerName',
                                    'Department',
                                    'PostCode',
                                    'PrefecturesCode__prefecturename',
                                    'Municipalities',
                                    'Address',
                                    'BuildingName',
                                    'ClosingDate',
                                    'LastClaimBalance',
                            ))

    return Customer

def PrevBalance(lastdate, Customer, FromDate, ToDate): 
    #前月までの入金額計
    queryset = Deposit.objects.filter(DepositDate__lte=(str(lastdate)),DepositCustomerCode=(str(Customer[0]['id'])))
    DepoPrvSum = list(queryset.values('DepositCustomerCode').annotate(Depo_total=Coalesce(Sum('DepositMoney'),0,output_field=DecimalField())))
    #0判定
    if DepoPrvSum:
        DepoPrvTotal = int(DepoPrvSum[0]['Depo_total'])
    else:
        DepoPrvTotal = 0
    #前月までの売上額計
    queryset =  RequestResult.objects.filter(ResultDate__lte=(str(lastdate)),
                OrderingId__CustomeCode=(str(Customer[0]['id'])),
                InvoiceNUmber__gt=0,
                InvoiceIssueDiv=1
                )
    SellPrvSum =  list(queryset.values('OrderingId__CustomeCode').annotate(
        Abs_total=Sum(Abs(Coalesce(F('ShippingVolume'),0) * Coalesce(F('OrderingDetailId__DetailSellPrice'),0)),output_field=DecimalField())))
    #0判定
    if SellPrvSum:
        SellPrvTotal = int(SellPrvSum[0]['Abs_total'])
        SellPrvtax = int(SellPrvSum[0]['Abs_total']) * 0.1
    else:
        SellPrvTotal = 0
        SellPrvtax = 0
    #前回請求額算出
    PrevBill = int(Customer[0]['LastClaimBalance']) - int(DepoPrvTotal) + int(SellPrvTotal) + int(SellPrvtax)
    #請求月入金合計額
    queryset = Deposit.objects.filter(DepositDate__range=(str(FromDate),str(ToDate)),DepositCustomerCode=(str(Customer[0]['id'])))
    DepoSum = list(queryset.values('DepositCustomerCode').annotate(Depo_total=Coalesce(Sum('DepositMoney'),0,output_field=DecimalField())))
    #0判定
    if DepoSum:
        DepoTotal = int(DepoSum[0]['Depo_total'])
    else:
        DepoTotal = 0
    #繰越額
    CarryForward = int(PrevBill) - int(DepoTotal)   
    #請求月売上合計額
    queryset =  RequestResult.objects.filter(ResultDate__range=(str(FromDate),str(ToDate)),
                OrderingId__CustomeCode=(str(Customer[0]['id'])),
                InvoiceNUmber__gt=0,
                InvoiceIssueDiv=1
                )

    SellSum =  list(queryset.values('OrderingId__CustomeCode').annotate(
        Abs_total=Sum(Abs(Coalesce(F('ShippingVolume'),0) * Coalesce(F('OrderingDetailId__DetailSellPrice'),0)),output_field=DecimalField())))
    #0判定
    if SellSum:
        SellTotal = int(SellSum[0]['Abs_total'])
    else:
        SellTotal = 0
    #請求月売上消費税額
    tax = int(SellTotal) * 0.1
    #今回請求額
    invoice = int(CarryForward) + int(SellTotal) + int(tax)
    return(PrevBill, DepoTotal, CarryForward, SellTotal, tax, invoice)

def Detail(Customer, FromDate, ToDate ): 
    #請求月売上レコード
    queryset =  RequestResult.objects.filter(ResultDate__range=(str(FromDate),str(ToDate)),
                OrderingId__CustomeCode=(str(Customer[0]['id'])),
                InvoiceNUmber__gt=0,
                InvoiceIssueDiv=1
                )
    queryset =  queryset.values('InvoiceNUmber','OrderingId__CustomeCode','OrderingId__SlipDiv','OrderingId__OrderNumber',
                                'OrderingId__CustomeCode_id__CustomerName','OrderingId__ProductName','OrderingId__OrderingCount',
                                'ShippingDate','ResultDate').annotate(
                                    Abs_total=Sum(Abs(F("ShippingVolume") * F("OrderingDetailId__DetailSellPrice"))),
                                    Shipping_total=Sum('ShippingVolume')
                                    )

    queryset =  queryset.values_list(
         'ResultDate',
         'InvoiceNUmber',
         'OrderingId__ProductName',
         'OrderingId__OrderingCount',
         'Shipping_total',
         'Abs_total',
    )

    #請求月入金レコード
    queryset_depo = Deposit.objects.filter(DepositDate__range=(str(FromDate),str(ToDate)),DepositCustomerCode=(str(Customer[0]['id'])))
    queryset_depo = queryset_depo.values_list('DepositDate','DepositSummary','DepositDiv__DepoPayDivname','DepositSummary','DepositSummary','DepositMoney')
 
    #繰越レコードと売上レコードと入金レコードを結合
    result = list(chain(queryset, queryset_depo))

    return result

def print_string(pdf_canvas, dt_own, dt, billdate, dt_Prev, dt_Detail, Date_From):
    rec = len(dt)
    req = math.ceil(rec/40)
    k = 0

    for i in range(req):
        # フォント登録
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
        # 用紙サイズ
        width, height = A4
        # title
        font_size = 16
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(260, 800, '請　求　書')
        # 請求先
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(40, 795, '〒 ' + dt[i]['PostCode'])
        pdf_canvas.drawString(55, 785, dt[i]['PrefecturesCode__prefecturename'] + dt[i]['Municipalities'] + dt[i]['Address'])
        pdf_canvas.drawString(60, 770, dt[i]['BuildingName'])
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(55, 740, dt[i]['CustomerName'] + '　' + '様')

        data =[['締日','請求日'],
               [dt[i]['ClosingDate'],billdate],
              ]

        table = Table(data, colWidths=(15*mm, 30*mm), rowHeights=(4*mm, 6*mm))
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 9),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 1), (1, 1), 'MIDDLE'),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 157*mm, 275.0*mm)

        # 登録番号
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(463, 770, '登録番号：T2030001124438')
        # 自社情報
        # ロゴ追加
        #img = './mysite/myapp/templates/image/image1.jpg'
        #img = './static/image/image1.jpg'
        #pdf_canvas.drawImage(img, 142*mm, 260*mm , 30*mm, 10*mm)
        # 自社名
        font_size = 16
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(430, 735, dt_own[0]['CustomerName'])
        # 自社住所
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 720, dt_own[0]['PrefecturesCode__prefecturename'] + dt_own[0]['Municipalities'] + 
                              dt_own[0]['Address'] + dt_own[0]['BuildingName'])
        pdf_canvas.drawString(400, 710, 'TEL: ' + dt_own[0]['PhoneNumber'] + '　FAX: ' + dt_own[0]['FaxNumber'])
        #取引銀行名
        font_size = 8
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 700, '取引銀行：　みずほ銀行青山支店　当座0131545')

        # 残高
        data =[['前回御請求額','御入金額','','繰越額','当月税抜御請求額10%対象','消費税額 10%'],
               ['{:,.0f}'.format(dt_Prev[0]), '{:,.0f}'.format(dt_Prev[1]), '', '{:,.0f}'.format(dt_Prev[2]),
                 '{:,.0f}'.format(dt_Prev[3]), '{:,.0f}'.format(dt_Prev[4])],
              ]

        table = Table(data, colWidths=(28*mm, 28*mm, 12*mm, 28*mm, 40*mm, 28*mm), rowHeights=(5*mm, 7*mm))
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (3, 0), 'HeiseiMin-W3', 9),
                ('FONT', (5, 0), (5, 0), 'HeiseiMin-W3', 9),
                ('FONT', (4, 0), (4, 0), 'HeiseiMin-W3', 8),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ('ALIGN', (0, 0), (5, 0), 'CENTER'),
                ('VALIGN', (0, 0), (5, 0), 'MIDDLE'),
                ('VALIGN', (0, 1), (5, 1), 'BOTTOM'),
                ('ALIGN', (0, 1), (5, 1), 'RIGHT'),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 230.0*mm)

        # 当月税込請求額
        data =[['当月税込御請求額'],
               ['{:,.0f}'.format(dt_Prev[5])],
              ]

        table = Table(data, colWidths=(25*mm), rowHeights=(5*mm, 7*mm))
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, 0), 'HeiseiMin-W3', 8),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                ('VALIGN', (0, 1), (0, 1), 'BOTTOM'),
                ('ALIGN', (0, 1), (5, 1), 'RIGHT'),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 177*mm, 230.0*mm)

        # 表題
        style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_CENTER)
        itemNo0 = Paragraph('年月日',style)
        itemNo1 = Paragraph('伝票番号',style)
        itemNo2 = Paragraph('区分',style)
        itemNo3 = Paragraph('品' + '&nbsp&nbsp' + '名',style)
        itemNo4 = Paragraph('数量',style)
        itemNo5 = Paragraph('単価',style)
        itemNo6 = Paragraph('税抜金額',style)
        itemNo7 = Paragraph('摘要',style)
        data = [
            [itemNo0, itemNo1, itemNo2, itemNo3, '', itemNo4, itemNo5, itemNo6, itemNo7],
        ]
        table = Table(data, colWidths=(18*mm, 18*mm, 10*mm, 45*mm, 15*mm, 21*mm, 21*mm, 25*mm, 20*mm), rowHeights=5.25*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('SPAN', (3, 0), (4, 0)),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 220.0*mm)

        data =[]
        l=len(dt_Detail)
        styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_LEFT)
        styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_RIGHT)
        styleCenter = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)

        #繰越
        Date_From = datetime.datetime.strptime(Date_From, '%Y-%m-%d') 
        ResultDate = Paragraph(Date_From.strftime('%y%m%d'),styleCenter)
        InvoiceNumber = Paragraph('',styleCenter)
        ProductName = Paragraph('繰越',styleLeft)
        ShippingVolume = Paragraph('',styleRight)      
        Prceeds = Paragraph(f"{int(dt_Prev[0]):,}",styleRight)

        data = [
                [ResultDate, InvoiceNumber, '', ProductName, '', ShippingVolume, '', Prceeds, ''],
        ]

        table = Table(data, colWidths=(18*mm, 18*mm, 10*mm, 45*mm, 15*mm, 21*mm, 21*mm, 25*mm, 20*mm), rowHeights=5.25*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

        #table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        #table.drawOn(pdf_canvas, 10*mm, 210.0*mm)

        k=0
        rowlg=40
        while k < rowlg:
            if k<l:
                row = dt_Detail[k]            

                ResultDate = Paragraph(row[0].strftime('%y%m%d'),styleCenter)
                InvoiceNumber = Paragraph(row[1],styleCenter)
                ProductName = Paragraph(row[2],styleLeft)
                if row[4]=='':
                    ShippingVolume = Paragraph(row[4],styleRight)
                else:
                    ShippingVolume = Paragraph('{:,.2f}'.format(row[4]),styleRight)
                
                Prceeds = Paragraph(f"{int(row[5]):,}",styleRight)
                OrderingCount = Paragraph(row[3],styleRight)
                data += [
                        [ResultDate, InvoiceNumber, '', ProductName, OrderingCount, ShippingVolume, '', Prceeds, ''],
                ]
            else:
                data += [
                        ['','','','','','','','',''],
                ]

            table = Table(data, colWidths=(18*mm, 18*mm, 10*mm, 45*mm, 15*mm, 21*mm, 21*mm, 25*mm, 20*mm), rowHeights=5.25*mm)
            table.setStyle(TableStyle([
                    ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                    #('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                    ('LINEBEFORE', (0, 0), (0, 40), 0.50, colors.black),
                    ('LINEBEFORE', (1, 0), (1, 40), 0.50, colors.black),
                    ('LINEBEFORE', (2, 0), (2, 40), 0.50, colors.black),
                    ('LINEBEFORE', (3, 0), (3, 40), 0.50, colors.black),
                    ('LINEBEFORE', (5, 0), (5, 40), 0.50, colors.black),
                    ('LINEBEFORE', (6, 0), (6, 40), 0.50, colors.black),
                    ('LINEBEFORE', (7, 0), (7, 40), 0.50, colors.black),
                    ('LINEBEFORE', (8, 0), (8, 40), 0.50, colors.black),
                    ('LINEAFTER' , (8, 0), (8, 40), 0.50, colors.black),
                    ('LINEBELOW' , (0, 0), (8, 40), 0.50, colors.black),
                    #('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
            # 変数加算
            k += 1

        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 4.5*mm)

        pdf_canvas.showPage()
if __name__ == '__main__':
    make()   
