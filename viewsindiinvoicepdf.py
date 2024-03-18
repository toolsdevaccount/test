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
# 計算用
from decimal import Decimal
import math
# メッセージ
from django.contrib import messages
#LOG出力設定
import logging
logger = logging.getLogger(__name__)

def pdf(request,pkfrom,pkto,isdate):
    try:
        strtime = timezone.now() + datetime.timedelta(hours=9)
        filename = "IndividualInvoice_" + strtime.strftime('%Y%m%d%H%M%S')
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
        pkfromdef = pkfrom  # 個別請求書番号初期値をコピー
        make(pkfrom,pkto,isdate,response)
        cnt = 0
        cnt = pkto - pkfromdef +1
        for i in range(cnt):
            if i>0:
                pkfromdef+= 1
            UpdateQuery(pkfromdef,isdate)

    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        logger.error(message)
        messages.add_message(request, messages.ERROR, message)
        return redirect("myapp:individualinvoicelist")
    return response

def make(pkfrom,pkto,isdate,response):
    pdf_canvas = set_info(response) # キャンバス名
    cnt = pkto - pkfrom +1
    for i in range(cnt):
        if i>0:
            pkfrom+= 1     
        dt = connect(pkfrom,isdate)
        print_string(pdf_canvas,dt)
   
    pdf_canvas.save() # 保存

#個別請求書
def set_info(response):
    pdf_canvas = canvas.Canvas(response,pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("納品書")
    pdf_canvas.setSubject("納品書")
    return pdf_canvas

def UpdateQuery(pkfromdef,isdate):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
           ' UPDATE ' 
	           ' myapp_requestresult '
	       ' SET ' 	 
		       '  InvoiceIssueDate = DATE_FORMAT(' + str(isdate) + ' ,"%Y-%m-%d" )'
               ' ,InvoiceIssueDiv = true '
	       ' WHERE '
		        ' INVOICENumber = ' + str(pkfromdef) 
        )
    cur.execute(sql)
    result = conn.affected_rows()
    conn.commit()

    cur.close()
    conn.close()

    return result

def connect(pkfrom,isdate):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
        ' SELECT '
        '	 C.InvoiceNUmber '
        '	,CONCAT(A.SlipDiv,"-",A.OrderNumber) 		        AS OrderNumber '
        '	,D.CustomerName 							        AS CustomerName '
        '	,D.PostCode '
        '	,H.prefecturename '
        '	,D.Municipalities '
        '	,D.Address '
        '	,D.BuildingName '
        '	,E.CustomerName 							        AS ShippingName '
        '	,DATE_FORMAT(ShippingDate,"%y%m%d")	                AS ShippingDate '
        '	,A.ProductName '
        '	,A.OrderingCount '
        '	,B.DetailColorNumber '
        '	,B.DetailColor '
        '	,FORMAT(C.ShippingVolume,2) '
        '	,FORMAT(B.DetailSellPrice,0) '
        '	,FORMAT(C.ShippingVolume * B.DetailSellPrice,0)	    AS SellPrice '
        '	,F.CustomerName '
        '	,F.PostCode '
        '	,G.prefecturename '
        '	,F.Municipalities '
        '	,F.Address '
        '	,F.BuildingName '
        '	,F.PhoneNumber '
        '	,F.FaxNumber '
        '	,C.ShippingVolume * B.DetailSellPrice '
        '   ,CASE WHEN B.DetailUnitDiv=1 THEN "㎏" WHEN B.DetailUnitDiv=2 THEN "本" ELSE " " END'
        '   ,C.ResultSummary'
        '	,DATE_FORMAT(' + str(isdate) + ',"%Y年%m月%d日")	AS issuedate '
        '   ,D.id'
        ' FROM '
        '	myapp_orderingtable A '
        '	INNER JOIN '
        '	myapp_orderingdetail B ON '
        '		A.id = B.OrderingTableId_id '
        '	INNER JOIN '
        '	myapp_requestresult C ON '
        '		 A.id = C.OrderingId_id '
        '	AND B.id = C.OrderingDetailId_id '
        '	LEFT JOIN '
        '	myapp_customersupplier D ON '
        '		A.CustomeCode_id = D.id '
        '	LEFT JOIN '
        '	myapp_prefecture H on '
        '		D.PrefecturesCode_id = H.id '
        '	LEFT JOIN '
        '	myapp_customersupplier E ON '
        '		A.ShippingCode_id = E.id '
        '	,(SELECT PostCode,CustomerName,PrefecturesCode_id,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber FROM myapp_customersupplier WHERE CustomerCode = "A0042" AND is_Deleted = 0) F '
        '	LEFT JOIN '
        '	myapp_prefecture G on '
        '		F.PrefecturesCode_id = G.id '
        ' WHERE '
        '	  C.INVOICENumber = ' + str(pkfrom) + 
        ' ORDER BY '
        '	C.id ASC '
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def print_string(pdf_canvas,dt):
    rec = len(dt)
    req = math.ceil(rec/9)
    k = 0

    for i in range(req):
        # フォント登録
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
        # 用紙サイズ
        width, height = A4
        # 線の太さ
        pdf_canvas.setLineWidth(0.25)
        # title
        font_size = 14
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(260, 820, '納　品　書')
        # 請求先
        font_size = 11
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(40, 815, '〒 ' + dt[0][3])
        pdf_canvas.drawString(55, 805, dt[0][4] + dt[0][5] + dt[0][6])
        pdf_canvas.drawString(60, 795, dt[0][7])
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(55, 760, dt[0][8] + '　' + '様')
        # 個別請求番号
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 820, 'NO. ' + dt[0][0])
        # 発行日
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(500, 810, dt[0][28])
        # 登録番号
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(430, 790, '登録番号：T2030001124436')
        # 自社情報
        # ロゴ追加
        img = './mysite/myapp/templates/image/image1.jpg'
        #img = './static/image/image1.jpg'
        pdf_canvas.drawImage(img, 142*mm, 267*mm , 30*mm, 10*mm)
        # 自社住所
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 745, dt[0][19] + dt[0][20] + dt[0][21] + dt[0][22])
        pdf_canvas.drawString(400, 735, 'TEL: ' + dt[0][23] + '　FAX: ' + dt[0][24])
        #取引銀行名
        font_size = 8
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 725, '取引銀行：　みずほ銀行青山支店　当座0131545')
        # 出荷先
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(220, 730, '出荷先　' +  dt[0][8])
        # 品名、番手、色番、色名、数量、単位、単価、希望納期、回答納期、備考(中央寄せ)
        style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_CENTER)
        itemNo0 = Paragraph('出荷日',style)
        itemNo1 = Paragraph('品' + '&nbsp&nbsp' + '名',style)
        itemNo2 = Paragraph('数量',style)
        itemNo3 = Paragraph('単位',style)
        itemNo4 = Paragraph('単価',style)
        itemNo5 = Paragraph('金額',style)
        itemNo6 = Paragraph('摘' + '&nbsp&nbsp&nbsp' + '要',style)
        data = [
            [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4, itemNo5, itemNo6],
        ]
        table = Table(data, colWidths=(15*mm, 55*mm, 18*mm, 10*mm, 20*mm, 20*mm, 55*mm), rowHeights=8*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 245.5*mm)

        data =[]
        l=len(dt)
        total=0
        styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_LEFT)
        styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_RIGHT)
        styleCenter = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)

        if i==0:
            k=0
        else:
            k = i*9
        rowlg = (i+1)*9
        
        while k < rowlg:
            if k<l:
                row = dt[k]
                # 合計計算
                total += Decimal(row[25])

                ShippingDate = Paragraph(row[9],styleCenter)
                ProductName = Paragraph(row[10] + '<br/>\n' + row[12],styleLeft)
                OrderingCount = Paragraph(row[11],styleLeft)
                DetailColor = Paragraph(row[13],styleLeft)
                ShippingVolume = Paragraph(row[14],styleRight)
                DetailSellPrice = Paragraph(row[15],styleRight)
                DetailUnitDiv = Paragraph(row[26],styleCenter)
                SellPrice = Paragraph(row[16],styleRight)
                ResultSummary = Paragraph(row[27],styleLeft)
                OrderNumber = Paragraph(row[1],styleLeft)
                # 0なら空白を送る
                if row[14] == '0.00':
                    varivol = ' '
                else:
                    varivol = row[14]
                ShippingVolume = Paragraph(varivol,styleRight)
                # 0なら空白を送る
                if row[16] == '0':
                    variPrice = ' '
                else:
                    variPrice = row[16]

                SellPrice = Paragraph(variPrice,styleRight)

                data += [
                        [ShippingDate, ProductName, DetailColor, OrderingCount, ShippingVolume, DetailUnitDiv, DetailSellPrice, SellPrice, ResultSummary],
                ]
            else:
                data += [
                        ['','','','','','','','',''],
                ]

            table = Table(data, colWidths=(15*mm, 22.5*mm, 17.5*mm, 15.0*mm, 18*mm, 10*mm, 20*mm, 20*mm, 55*mm), rowHeights=8.5*mm)
            table.setStyle(TableStyle([
                    #('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 11),
                    ('LINEBEFORE', (0, 0), (0, 8), 0.50, colors.black),
                    ('LINEBEFORE', (1, 0), (1, 8), 0.50, colors.black),
                    ('LINEBEFORE', (4, 0), (4, 8), 0.50, colors.black),
                    ('LINEBEFORE', (5, 0), (5, 8), 0.50, colors.black),
                    ('LINEBEFORE', (6, 0), (6, 8), 0.50, colors.black),
                    ('LINEBEFORE', (7, 0), (7, 8), 0.50, colors.black),
                    ('LINEBEFORE', (8, 0), (8, 8), 0.50, colors.black),
                    ('LINEAFTER' , (8, 0), (8, 8), 0.50, colors.black),
                    ('LINEBELOW' , (0, 0), (8, 7), 0.50, colors.black),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ('VALIGN', (1, 0), (1, 8), 'TOP'),
                    ('VALIGN', (2, 0), (2, 8), 'BOTTOM'),
                    ('VALIGN', (3, 0), (3, 8), 'TOP'),
                ]))
            # 変数加算
            k += 1

        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 169.0*mm)

        # 合計
        itemNo7 = Paragraph('10%対象税抜合計',styleRight)
        itemNo8 = Paragraph(str(f"{int(total):,}"),styleRight)

        data = [
            [itemNo7, itemNo8, OrderNumber],
        ]

        table = Table(data, colWidths=(118*mm, 20*mm, 55*mm), rowHeights=8*mm)
        table.setStyle(TableStyle([
                #('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 11),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 161.1*mm)
        #--------------------------------------------------------------------------------------------------------#
        # 控出力
        #--------------------------------------------------------------------------------------------------------#
        # title
        font_size = 14
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(260, 380, '納　品　書(控)')
        # 請求先
        font_size = 11
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(40, 375, '〒 ' + dt[0][3])
        pdf_canvas.drawString(55, 365, dt[0][4] + dt[0][5] + dt[0][6])
        pdf_canvas.drawString(60, 355, dt[0][7])
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(55, 320, dt[0][8] + '　' + '様')
        # 個別請求番号
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 380, 'NO. ' + dt[0][0])
        # 発行日
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(500, 370, dt[0][28])
        # 登録番号
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(430, 350, '登録番号：T2030001124436')
        # 自社情報
        # ロゴ追加
        img = './mysite/myapp/templates/image/image1.jpg'
        #img = './static/image/image1.jpg'
        pdf_canvas.drawImage(img, 142*mm, 112*mm , 30*mm, 10*mm)
        #自社住所
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 305, dt[0][19] + dt[0][20] + dt[0][21] + dt[0][22])
        pdf_canvas.drawString(400, 295, 'TEL: ' + dt[0][23] + '　FAX: ' + dt[0][24])
        #取引銀行名
        font_size = 8
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 285, '取引銀行：　みずほ銀行青山支店　当座0131545')
        # 出荷先
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(220, 290, '出荷先　' +  dt[0][8])
        # 出荷日、品名、数量、単位、単価、金額、摘要
        data = [
            [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4, itemNo5, itemNo6],
        ]
        table = Table(data, colWidths=(15*mm, 55*mm, 18*mm, 10*mm, 20*mm, 20*mm, 55*mm), rowHeights=8*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 11),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 90.0*mm)

        data =[]
        l=len(dt)
        total=0
        if i==0:
            k=0
        else:
            k = i*9
        rowlg = (i+1)*9
        
        while k < rowlg:
            if k<l: 
                row = dt[k]
                #合計計算
                total += Decimal(row[25])

                ShippingDate = Paragraph(row[9],styleCenter)

                ProductName = Paragraph(row[10] + '<br/>\n' + row[12],styleLeft)
                OrderingCount = Paragraph(row[11],styleLeft)
                DetailColor = Paragraph(row[13],styleLeft)

                ShippingVolume = Paragraph(row[14],styleRight)
                DetailSellPrice = Paragraph(row[15],styleRight)
                DetailUnitDiv = Paragraph(row[26],styleCenter)
                SellPrice = Paragraph(row[16],styleRight)
                ResultSummary = Paragraph(row[27],styleLeft)
                OrderNumber = Paragraph(row[1],styleLeft)
                # 0なら空白を送る
                if row[14] == '0.00':
                    varivol = ' '
                else:
                    varivol = row[14]
                ShippingVolume = Paragraph(varivol,styleRight)

                # 0なら空白を送る
                if row[16] == '0':
                    variPrice = ' '
                else:
                    variPrice = row[16]

                SellPrice = Paragraph(variPrice,styleRight)

                data += [
                        [ShippingDate, ProductName, DetailColor, OrderingCount, ShippingVolume, DetailUnitDiv, DetailSellPrice, SellPrice, ResultSummary],
                ]
            else:
                data += [
                        ['','','','','','','','',''],
                ]

            table = Table(data, colWidths=(15*mm, 22.5*mm, 17.5*mm, 15.0*mm, 18*mm, 10*mm, 20*mm, 20*mm, 55*mm), rowHeights=8.5*mm)
            table.setStyle(TableStyle([
                    ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 11),
                    ('LINEBEFORE', (0, 0), (0, 8), 0.50, colors.black),
                    ('LINEBEFORE', (1, 0), (1, 8), 0.50, colors.black),
                    ('LINEBEFORE', (4, 0), (4, 8), 0.50, colors.black),
                    ('LINEBEFORE', (5, 0), (5, 8), 0.50, colors.black),
                    ('LINEBEFORE', (6, 0), (6, 8), 0.50, colors.black),
                    ('LINEBEFORE', (7, 0), (7, 8), 0.50, colors.black),
                    ('LINEBEFORE', (8, 0), (8, 8), 0.50, colors.black),
                    ('LINEAFTER' , (8, 0), (8, 8), 0.50, colors.black),
                    ('LINEBELOW' , (0, 0), (8, 7), 0.50, colors.black),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ('VALIGN', (1, 0), (1, 8), 'TOP'),
                    ('VALIGN', (2, 0), (2, 8), 'BOTTOM'),
                    ('VALIGN', (3, 0), (3, 8), 'TOP'),
                ]))
            k += 1

        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 13.5*mm)

        # 合計
        itemNo7 = Paragraph('10%対象税抜合計',styleRight)
        itemNo8 = Paragraph(str(f"{int(total):,}"),styleRight)

        data = [
            [itemNo7, itemNo8, OrderNumber],
        ]

        table = Table(data, colWidths=(118*mm, 20*mm, 55*mm), rowHeights=8*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 11),
                ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ]))
        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 5.5*mm)

        pdf_canvas.showPage()
if __name__ == '__main__':
    make()   
