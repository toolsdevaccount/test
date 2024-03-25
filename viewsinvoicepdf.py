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
# MySQL
import MySQLdb
# 日時
from django.utils import timezone
import datetime
from dateutil import relativedelta
# 計算用
from decimal import Decimal
import math
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
        tdate = datetime.datetime.strptime(str(invoiceDate_To), '%Y%m%d')
        invoiceDate_From = datetime.datetime.strptime(str(invoiceDate_From), '%Y%m%d') 
        invoiceDate_To = datetime.datetime.strptime(str(invoiceDate_To), '%Y%m%d')
        # 前月同日を算出する
        lastdate = tdate - relativedelta.relativedelta(months=1)
        # 日付型に変換する
        lastdate = lastdate.strftime('%Y-%m-%d')
        invoiceDate_From = invoiceDate_From.strftime('%Y-%m-%d') 
        invoiceDate_To = invoiceDate_To.strftime('%Y-%m-%d') 

        make(pkclosing, invoiceDate_From, invoiceDate_To, element_From, element_To, lastdate, response)
        #UpdateQuery()

    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        logger.error(message)
        messages.add_message(request, messages.ERROR, message)
        return redirect("myapp:invoicelist")
    return response

def make(closing, invoiceDate_From, invoiceDate_To, element_From, element_To, lastdate, response):
    pdf_canvas = set_info(response) # キャンバス名
    dt = customer(invoiceDate_To, element_From, element_To)
    dt_PrevBalance = PrevBalance(element_From, lastdate, invoiceDate_From, invoiceDate_To)
    dt_Detail = Detail(element_From, invoiceDate_From, invoiceDate_To)
    print_string(pdf_canvas, dt, dt_PrevBalance, dt_Detail)
   
    pdf_canvas.save() # 保存

#一括請求書
def set_info(response):
    pdf_canvas = canvas.Canvas(response,pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("一括請求書")
    pdf_canvas.setSubject("一括請求書")
    return pdf_canvas

def customer(invoiceDate_To, element_From, element_To):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
        ' SELECT '
        ' 	 A.id '
        '	,A.CustomerCode '
        '	,A.CustomerName '
        '	,A.Department '
        '	,A.PostCode '
        '	,B.prefecturename '
        '	,A.Municipalities '
        '	,A.Address '
        '	,A.BuildingName '
        '	,A.ClosingDate '
        '	,A.LastClaimBalance '
        '	,C.CustomerName '
        '	,C.PostCode '
        '	,D.prefecturename '
        '	,C.Municipalities '
        '	,C.Address '
        '	,C.BuildingName '
        '	,C.PhoneNumber '
        '	,C.FaxNumber '
        '	,DATE_FORMAT("' + str(invoiceDate_To) + '","%Y年%m月%d日")	AS issuedate '
        ' FROM '
        '	myapp_customersupplier A '
        '	LEFT JOIN '
        '	myapp_prefecture B on '
        '		A.PrefecturesCode_id = B.id '
        '	,(SELECT PostCode,CustomerName,PrefecturesCode_id,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber FROM myapp_customersupplier WHERE CustomerCode = "A0042" AND is_Deleted = 0) C '
        '	LEFT JOIN '
        '	myapp_prefecture D on '
        '		C.PrefecturesCode_id = D.id '
        ' WHERE '
        '	  A.CustomerCode BETWEEN "' + str(element_From) + '" AND "' + str(element_To) + '"'
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def PrevBalance(element_From, lastdate, invoiceDate_From, invoiceDate_To):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
        '	SELECT '
        '		 A.id '
        '		,A.CustomerCode '
        '		,FORMAT(A.LastClaimBalance - A.LastDepositMoney + B.LastSellPrice,0)		AS LastClaimBalance '
        '		,FORMAT(C.DepositMoney,0) AS DepositMoney '
        '		,FORMAT(A.LastClaimBalance - A.LastDepositMoney + B.LastSellPrice - C.DepositMoney,0) AS CarryForward '
        '		,FORMAT(D.SellPrice,0) AS SellPrice '
        '		,FORMAT(ROUND(D.SellPrice * 0.1,0),0)	AS TAX '
        '		,FORMAT((D.SellPrice + ROUND(D.SellPrice * 0.1,0)) + A.LastClaimBalance - A.LastDepositMoney + B.LastSellPrice - C.DepositMoney,0) AS Proceeds '
        '	FROM '
        '		( '
        '		SELECT ' 
        '			 B.id '
        '			,B.CustomerCode '
        '			,B.LastClaimBalance '
        '			,SUM(A.DepositMoney)		AS LastDepositMoney '
        '		FROM '
        '			myapp_deposit A ' 
        '			left join ' 
        '			myapp_customersupplier B on '
        '				A.DepositCustomerCode_id = B.id '
        '		WHERE '
        '			 B.CustomerCode = "' + str(element_From) + '"'
        '		AND A.DepositDate <= "' + str(lastdate) + '"'
        '		GROUP BY '
        '			B.id '
        '		) A, '
        '		( '
        '			SELECT '
        '			 D.id '
        '			,D.CustomerCode '
        '			,SUM(A.ShippingVolume * C.DetailSellPrice) AS LastSellPrice '
        '		FROM '
        '			myapp_requestresult A ' 
        '			INNER JOIN '
        '			myapp_orderingtable B ON '
        '				A.OrderingId_id = B.id '
        '			INNER JOIN '
        '			myapp_orderingdetail C ON '
        '				A.OrderingDetailId_id = C.id '
        '			LEFT JOIN '
        '			myapp_customersupplier D on '
        '				B.CustomeCode_id = D.id '
        '		 WHERE '
        '			 D.CustomerCode = "' + str(element_From) + '"' 
        '		AND A.ShippingDate <= "' + str(lastdate) + '"' 
        '		GROUP BY '
        '			D.id '
        '		) B, '
        '			( '
        '		SELECT ' 
        '			 B.id '
        '			,B.CustomerCode '
        '			,B.LastClaimBalance '
        '			,SUM(A.DepositMoney)		AS DepositMoney '
        '		FROM ' 
        '			myapp_deposit A ' 
        '			left join ' 
        '			myapp_customersupplier B on '
        '				A.DepositCustomerCode_id = B.id '
        '		WHERE '
        '			 B.CustomerCode = "' + str(element_From) + '"'
        '		AND A.DepositDate BETWEEN "' + str(invoiceDate_From) + '" AND "' + str(invoiceDate_To) + '"' 
        '		GROUP BY '
        '			B.id '
        '		) C, '
        '		( '
        '			SELECT '
        '			 D.id '
        '			,D.CustomerCode '
        '			,SUM(A.ShippingVolume * C.DetailSellPrice) AS SellPrice '
        '		FROM '
        '			myapp_requestresult A ' 
        '			INNER JOIN '
        '			myapp_orderingtable B ON '
        '				A.OrderingId_id = B.id '
        '			INNER JOIN ' 
        '			myapp_orderingdetail C ON '
        '				A.OrderingDetailId_id = C.id '
        '			LEFT JOIN '
        '			myapp_customersupplier D on '
        '				B.CustomeCode_id = D.id '
        '		 WHERE '
        '			 D.CustomerCode = "' + str(element_From) + '"'
        '		AND A.ShippingDate BETWEEN "' + str(invoiceDate_From) + '" AND "' + str(invoiceDate_To) + '"' 
        '		GROUP BY '
        '			D.id '
        '		) D '
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def Detail(element_From, invoiceDate_From, invoiceDate_To):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
        ' SELECT '
        '		 DATE_FORMAT(A.ShippingDate,"%y%m%d")	AS ShippingDate '
        '		,A.InvoiceNUmber						AS InvoiceNumber '
        '		,B.ProductName							AS ProductName '
        '		,B.OrderingCount						AS OrderingCount '
        '		,A.ShippingVolume						AS ShippingVolume '
        '		,A.ShippingVolume * C.DetailSellPrice	AS Proceeds '
        ' FROM '
        '		myapp_requestresult A '
        '		INNER JOIN '
        '		myapp_orderingtable B ON '
        '			A.OrderingId_id = B.id '
        '		INNER JOIN '
        '		myapp_orderingdetail C ON '
        '			A.OrderingDetailId_id = C.id '
        '		LEFT JOIN '
        '		myapp_customersupplier D ON '
        '			B.CustomeCode_id = D.id '
        ' WHERE '
        '	  D.CustomerCode = "' + str(element_From) + '"'
        ' AND A.ShippingDate BETWEEN "' + str(invoiceDate_From) + '" AND "' + str(invoiceDate_To) + '"'
        ' UNION ALL '
        ' SELECT '
        '		 DATE_FORMAT(A.DepositDate,"%y%m%d") ' 
        '		,"" '
        '		,C.DepoPayDivname ' 
        '		,"" '
        '		,"" '
        '		,A.DepositMoney			AS DepositMoney ' 
        ' FROM '
        '	myapp_deposit A '
        '	LEFT JOIN '
        '	myapp_customersupplier B on '
        '		A.DepositCustomerCode_id = B.id '
        '	LEFT JOIN '
        '	myapp_depopaydiv C on '
        '		A.DepositDiv_id = C.DepoPayDivcode '
        ' WHERE '
        '	  B.CustomerCode = "' + str(element_From) + '"'
        ' AND A.DepositDate BETWEEN "' + str(invoiceDate_From) + '" AND "' + str(invoiceDate_To) + '"'
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result


def print_string(pdf_canvas,dt,dt_PrevBalance,dt_Detail):
    rec = len(dt)
    req = math.ceil(rec/9)
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
        pdf_canvas.drawString(40, 795, '〒 ' + dt[0][4])
        pdf_canvas.drawString(55, 785, dt[0][5] + dt[0][6] + dt[0][7])
        pdf_canvas.drawString(60, 770, dt[0][8])
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(55, 740, dt[0][2] + '　' + '様')

        data =[['締日','請求日'],
               [dt[i][9],dt[i][19]],
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
        pdf_canvas.drawString(430, 735, dt[0][11])
        # 自社住所
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 720, dt[0][13] + dt[0][14] + dt[0][15] + dt[0][16])
        pdf_canvas.drawString(400, 710, 'TEL: ' + dt[0][17] + '　FAX: ' + dt[0][18])
        #取引銀行名
        font_size = 8
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 700, '取引銀行：　みずほ銀行青山支店　当座0131545')

        # 残高
        data =[['前回御請求額','御入金額','','繰越額','当月税抜御請求額10%対象','消費税額 10%'],
               [dt_PrevBalance[0][2], dt_PrevBalance[0][3], '', dt_PrevBalance[0][4], dt_PrevBalance[0][5], dt_PrevBalance[0][6]],
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
               [dt_PrevBalance[0][7]],
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
            [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4, itemNo5, itemNo6, itemNo7],
        ]
        table = Table(data, colWidths=(18*mm, 18*mm, 10*mm, 60*mm, 21*mm, 21*mm, 25*mm, 20*mm), rowHeights=5.25*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 220.0*mm)

        data =[]
        l=len(dt_Detail)
        styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_LEFT)
        styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_RIGHT)
        styleCenter = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)

        #if i==0:
        #    k=0
        #else:
        #    k = i*9
        #rowlg = (i+1)*9

        k=0
        rowlg=40
        
        while k < rowlg:
            if k<l:
                row = dt_Detail[k]

                ShippingDate = Paragraph(row[0],styleCenter)
                InvoiceNumber = Paragraph(row[1],styleCenter)
                ProductName = Paragraph(row[2],styleLeft)
                ShippingVolume = Paragraph(row[4],styleRight)
                Prceeds = Paragraph(f"{int(row[5]):,}",styleRight)

                data += [
                        [ShippingDate, InvoiceNumber, '', ProductName, ShippingVolume, '', Prceeds, ''],
                ]
            else:
                data += [
                        ['','','','','','','',''],
                ]

            table = Table(data, colWidths=(18*mm, 18*mm, 10*mm, 60*mm, 21*mm, 21*mm, 25*mm, 20*mm), rowHeights=5.25*mm)
            table.setStyle(TableStyle([
                    ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                    ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                    ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
            # 変数加算
            k += 1

        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 9.9*mm)

        pdf_canvas.showPage()
if __name__ == '__main__':
    make()   
