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

def pdf(request,pkclosing,invoiceDate_From,invoiceDate_To):
    try:
        strtime = timezone.now() + datetime.timedelta(hours=9)
        filename = "Invoice_" + strtime.strftime('%Y%m%d%H%M%S')
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
        #pkfromdef = pkfrom  # 一括請求書番号初期値をコピー
        make(pkclosing, invoiceDate_From, invoiceDate_To, response)
        #UpdateQuery()

    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        logger.error(message)
        messages.add_message(request, messages.ERROR, message)
        return redirect("myapp:invoicelist")
    return response

def make(pkclosing, invoiceDate_From, invoiceDate_To, response):
    pdf_canvas = set_info(response) # キャンバス名
    #cnt = pkto - pkfrom +1
    #for i in range(cnt):
    #    if i>0:
    #        pkfrom+= 1     
    dt = connect()
    print_string(pdf_canvas,dt)
   
    pdf_canvas.save() # 保存

#一括請求書
def set_info(response):
    pdf_canvas = canvas.Canvas(response,pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("一括請求書")
    pdf_canvas.setSubject("一括請求書")
    return pdf_canvas

def connect():
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
        '	,DATE_FORMAT(20240318,"%Y年%m月%d日")	AS issuedate '
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
        '	  C.INVOICENumber = 113635 ' 
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
        # title
        font_size = 16
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(260, 800, '請　求　書')
        # 請求先
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(40, 795, '〒 ' + dt[0][3])
        pdf_canvas.drawString(55, 785, dt[0][4] + dt[0][5] + dt[0][6])
        pdf_canvas.drawString(60, 770, dt[0][7])
        font_size = 12
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(55, 740, dt[0][8] + '　' + '様')

        data =[['締日','請求日'],
               ['30日締',dt[0][28]],
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
        pdf_canvas.drawString(430, 735, dt[0][17])
        # 自社住所
        font_size = 10
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 720, dt[0][19] + dt[0][20] + dt[0][21] + dt[0][22])
        pdf_canvas.drawString(400, 710, 'TEL: ' + dt[0][23] + '　FAX: ' + dt[0][24])
        #取引銀行名
        font_size = 8
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(400, 700, '取引銀行：　みずほ銀行青山支店　当座0131545')

        # 残高
        data =[['前回御請求額','御入金額','','繰越額','当月税抜御請求額10%対象','消費税額 10%'],
               ['10,000,000','10,000,000','','10,000,000','10,000,000','10,000,000'],
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
               ['19,339,796'],
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

        # 品名、番手、色番、色名、数量、単位、単価、希望納期、回答納期、備考(中央寄せ)
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
        l=len(dt)
        total=0
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
            #if k<l:
                #row = dt[k]
                # 合計計算
                #total += Decimal(row[25])

                #ShippingDate = Paragraph(row[9],styleCenter)
                #ProductName = Paragraph(row[10] + '<br/>\n' + row[12],styleLeft)
                #OrderingCount = Paragraph(row[11],styleLeft)
                #DetailColor = Paragraph(row[13],styleLeft)
                #ShippingVolume = Paragraph(row[14],styleRight)
                #DetailSellPrice = Paragraph(row[15],styleRight)
                #DetailUnitDiv = Paragraph(row[26],styleCenter)
                #SellPrice = Paragraph(row[16],styleRight)
                #ResultSummary = Paragraph(row[27],styleLeft)
                #OrderNumber = Paragraph(row[1],styleLeft)
                # 0なら空白を送る
                #if row[14] == '0.00':
                #    varivol = ' '
                #else:
                #    varivol = row[14]
                #ShippingVolume = Paragraph(varivol,styleRight)
                # 0なら空白を送る
                #if row[16] == '0':
                #    variPrice = ' '
                #else:
                #    variPrice = row[16]

                #SellPrice = Paragraph(variPrice,styleRight)

            #    data += [
            #            ['','','','','','','',''],
            #    ]
            #else:
            #    data += [
            #            ['','','','','','','',''],
            #    ]

            data += [
                    ['','','','','','','',''],
            ]

            table = Table(data, colWidths=(18*mm, 18*mm, 10*mm, 60*mm, 21*mm, 21*mm, 25*mm, 20*mm), rowHeights=5.25*mm)
            table.setStyle(TableStyle([
                    ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 10),
                    ('BOX', (0, 0), (-1, -1), 0.50, colors.black),
                    ('INNERGRID', (0, 0), (-1, -1), 0.50,  colors.black),
                ]))
            # 変数加算
            k += 1

        table.wrapOn(pdf_canvas, 10*mm, 10*mm)
        table.drawOn(pdf_canvas, 10*mm, 9.9*mm)

        pdf_canvas.showPage()
if __name__ == '__main__':
    make()   
