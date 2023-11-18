from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import B5, portrait, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
# MySQL
import MySQLdb
#from django.db import transaction
# 日時
from django.utils import timezone
import datetime
# 計算用
from decimal import Decimal
# メッセージ
from django.contrib import messages

def pdf(request,pk):
    try:
        strtime = timezone.now() + datetime.timedelta(hours=9)
        filename = "PurchaseOrder_" + strtime.strftime('%Y%m%d%H%M%S')
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'

        make(pk,response)
        UpdateQuery(pk)

    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        messages.error(request,message) 
        return redirect("myapp:orderinglist")
    return response

def make(pk,response):
    dt = connect(pk)
    if dt[0][43]==1:
        pdf_canvas = set_info(response) # キャンバス名
        print_string(pdf_canvas,dt)
    if dt[0][43]==2 or dt[0][43]==3:
        pdf_canvas = set_info_stain(response) # キャンバス名
        print_string_StainRequest(pdf_canvas,dt)
    pdf_canvas.save() # 保存

#発注書
def set_info(response):
    pdf_canvas = canvas.Canvas(response,pagesize=landscape(B5))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("発注書")
    pdf_canvas.setSubject("発注書")
    return pdf_canvas

#染色依頼書
def set_info_stain(response):
    pdf_canvas = canvas.Canvas(response,pagesize=portrait(B5))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("染色依頼書")
    pdf_canvas.setSubject("染色依頼書")
    return pdf_canvas

def UpdateQuery(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
           ' UPDATE ' 
	           ' myapp_orderingtable '
	       ' SET ' 	 
		       ' is_Ordered = true '
	       ' WHERE '
		        'id = ' + str(pk) 
        )
    cur.execute(sql)
    result = conn.affected_rows()
    conn.commit()

    cur.close()
    conn.close()

    return result

def connect(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
        ' SELECT '
        '    a.SlipDiv '
        '   ,a.OrderNumber '
        '   ,IFNULL(DATE_FORMAT(a.OrderingDate,"%Y年%m月%d日"),"") '
        '   ,a.ProductName '
        '   ,a.OrderingCount '
        '   ,a.StainPartNumber '
        '   ,a.SupplierPerson'
        '   ,CASE WHEN a.TitleDiv=1 THEN "様" ELSE "御中" END'
        '   ,IFNULL(DATE_FORMAT(b.StainAnswerDeadline,"%m/%d"),"") '
        '   ,c.CustomerName '
        '   ,c.PostCode '
        '   ,h.prefecturename '
        '   ,c.Municipalities '
        '   ,c.Address'
        '   ,c.BuildingName '
        '   ,b.DetailItemNumber '
        '   ,b.DetailColorNumber '
        '   ,b.DetailColor '
        '   ,b.DetailTailoring '
        '   ,FORMAT(b.DetailVolume,2) '
        '   ,FORMAT(b.detailunitprice,0)'
        '   ,b.detailsummary '
        '   ,"" '
        '   ,e.CustomerName '
        '   ,e.PostCode '
        '   ,g.prefecturename '
        '   ,e.Municipalities '
        '   ,e.Address'
        '   ,e.BuildingName '
        '   ,e.PhoneNumber '
        '   ,e.FaxNumber '
        '   ,d.first_name '
        '   ,d.last_name '
        '   ,d.email '
        '   ,f.CustomerName '
        '   ,f.PostCode '
        '   ,i.prefecturename '
        '   ,f.Municipalities'
        '   ,f.Address '
        '   ,f.BuildingName '
        '   ,f.PhoneNumber '
        '   ,f.FaxNumber '
        '   ,a.StainMixRatio '
        '   ,a.OutputDiv'
        '   ,IFNULL(DATE_FORMAT(a.StainShippingDate,"%Y年%m月%d日"),"") '
        '   ,IFNULL(DATE_FORMAT(b.SpecifyDeliveryDate,"%m/%d"),"") '
        '   ,j.CustomerName '
        '   ,k.CustomerName'
        '   ,CASE b.DetailUnitDiv ' 
        '       WHEN 1 THEN "㎏" '
        '       WHEN 2 THEN "本" '
        '       ELSE "" '
        '    END '
        '   ,l.CustomerName'
        ' FROM '
        '   myapp_orderingtable a '
        '   LEFT JOIN myapp_orderingdetail b on a.id = b.OrderingTableId_id'
        '   LEFT JOIN myapp_customersupplier c on a.RequestCode_id = c.id'
        '   LEFT JOIN auth_user d on a.ManagerCode = d.id'
        '   LEFT JOIN myapp_customersupplier f on a.ShippingCode_id = f.id'
        '   LEFT JOIN myapp_prefecture h on c.PrefecturesCode_id = h.id'
        '   LEFT JOIN myapp_prefecture i on f.PrefecturesCode_id = i.id'
        '   LEFT JOIN myapp_customersupplier j on a.SupplierCode_id = j.id'
        '   LEFT JOIN myapp_customersupplier k on a.StainShippingCode_id = k.id'
        '   LEFT JOIN myapp_customersupplier l on a.ApparelCode_id = l.id'
        '   ,(SELECT PostCode,CustomerName,PrefecturesCode_id,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber FROM myapp_customersupplier WHERE CustomerCode = "A00042" AND is_Deleted = 0) e'
        '   LEFT JOIN myapp_prefecture g on e.PrefecturesCode_id = g.id'
        ' WHERE a.id = ' + str(pk) + ' AND b.is_Deleted = 0 AND b.PrintDiv = 0' 
        ' ORDER BY '
        '   b.DetailItemNumber ASC' 
        )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def print_string(pdf_canvas,dt):
    # フォント登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    width, height = B5

    # 線の太さ
    pdf_canvas.setLineWidth(0.25)

    # 注文日
    font_size = 11
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(555, 430, dt[0][2])

    # title
    font_size = 16
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(308, 420, '発　　注　　書')

    # 発注先
    font_size = 12
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(80, 410, dt[0][46] + '　' + dt[0][6] + '　' + dt[0][7])

    # 出荷先
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(65, 360, '出荷先: ' + dt[0][34])
    pdf_canvas.drawString(65, 340, '〒 ' + dt[0][35])
    pdf_canvas.drawString(65, 330, dt[0][36] + dt[0][37] + dt[0][38] + dt[0][39])
    pdf_canvas.drawString(65, 320, 'TEL: ' + dt[0][40])

    # 自社情報
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)

    # ロゴ追加
    img = './mysite/myapp/templates/image/image1.jpg'
    #img = './static/image/image1.jpg'
    pdf_canvas.drawImage(img, 173*mm, 134*mm , 20*mm, 5*mm)

    pdf_canvas.drawString(560, 379, dt[0][31] + dt[0][32])
    pdf_canvas.drawString(490, 370, '〒 ' + dt[0][24])
    pdf_canvas.drawString(490, 360, dt[0][25] + dt[0][26] + dt[0][27] + dt[0][28])
    pdf_canvas.drawString(490, 350, 'TEL: ' + dt[0][29] + '　FAX: ' + dt[0][30])

    # オーダーNO
    font_size = 10
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(530, 325, 'オーダーNO: ')

    font_size = 11
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(590, 325, dt[0][0] + dt[0][1])
    # オーダーNO下線
    pdf_canvas.line(530, 318, 645, 318) 

    # 品名、番手、色番、色名、数量、単位、単価、希望納期、回答納期、備考(中央寄せ)
    style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_CENTER)
    itemNo0 = Paragraph('品' + '&nbsp&nbsp' + '名',style)
    itemNo1 = Paragraph('番手',style)
    itemNo2 = Paragraph('色番',style)
    itemNo3 = Paragraph('色' + '&nbsp&nbsp' + '名',style)
    itemNo4 = Paragraph('数量',style)
    itemNo5 = Paragraph('単位',style)
    itemNo6 = Paragraph('単価',style)
    itemNo7 = Paragraph('希望納期',style)
    itemNo8 = Paragraph('回答納期',style)
    itemNo9 = Paragraph('備' + '&nbsp&nbsp&nbsp' + '考',style)

    data = [
        [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4, itemNo5, itemNo6, itemNo7, itemNo8, itemNo9],
    ]

    table = Table(data, colWidths=(30*mm, 15*mm, 15*mm, 30*mm, 15*mm, 12*mm, 15*mm, 18*mm, 18*mm, 40*mm), rowHeights=7*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 8),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25,  colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 22.5*mm, 10*mm)
    table.drawOn(pdf_canvas, 22.5*mm, 103.0*mm)

    data =[]
    l=len(dt)
    Pname=''
    Ocnt=''
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_RIGHT)
    styleCenter = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_CENTER)

    for i in range(9):
        if i<l: 
            row = dt[i]
            # 前の行と同一品名の場合は空白
            if Pname == row[3]:
                ProductName = ''
            else:
                ProductName = Paragraph(row[3],styleLeft)

            # 前の行と同一番手の場合は空白
            if Ocnt == row[4]:
                OrderingCount = ''
            else:
                OrderingCount = Paragraph(row[4],styleLeft)

            DetailColorNumber = Paragraph(row[16],styleLeft)
            DetailColor = Paragraph(row[17],styleLeft)
            DetailSummary = Paragraph(row[21],styleLeft)
            # 指定した列の中央寄せ
            UnitDiv = Paragraph(row[48],styleCenter)
            StainAnswerDeadline = Paragraph(row[8],styleCenter)
            SpecifyDeliveryDate = Paragraph(row[45],styleCenter)
            # 指定した列の右寄せ
            Volume = Paragraph(row[19],styleRight)
            UnitPrice = Paragraph(row[20],styleRight)
            # 品名の保存
            Pname = row[3]
            # 番手の保存
            Ocnt = row[4]

            data += [
                    [ProductName, OrderingCount, DetailColorNumber, DetailColor, Volume, UnitDiv, UnitPrice, SpecifyDeliveryDate, StainAnswerDeadline, DetailSummary],
            ]
        else:
            data += [
                    ['','','','','','','','','',''],
            ]

        table = Table(data, colWidths=(30*mm, 15*mm, 15*mm, 30*mm, 15*mm, 12*mm, 15*mm, 18*mm, 18*mm, 40*mm), rowHeights=7*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 8),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))

    table.wrapOn(pdf_canvas, 22.5*mm, 10*mm)
    table.drawOn(pdf_canvas, 22.5*mm, 40.0*mm)

    # 摘要
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(65, 90, '摘要')

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(75, 80, '※単価の違いがございましたらお手数ですがご連絡ください。')

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(75, 70, '　出荷次第、オーダーNoを記入した納品書を翌日当社宛にご連絡ください。')

    # ロゴ追加
    img = './mysite/myapp/templates/image/image2.jpg'
    #img = './static/image/image2.jpg'
    pdf_canvas.drawImage(img, 110*mm, 8*mm, 32*mm, 7*mm)

    pdf_canvas.rect(63, 60, 591, 45) 

    pdf_canvas.showPage()
        
    if __name__ == '__main__':
        make()

def print_string_StainRequest(pdf_canvas,dt):
    # フォント登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    width, height = B5

    # title
    font_size = 16
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    if dt[0][43]==2:
        pdf_canvas.drawString(200, 650, '染 付 依 頼 書')
    if dt[0][43]==3:
        pdf_canvas.drawString(180, 650, 'ビ ー カ ー 染 付 依 頼 書')

    # 線の太さ
    pdf_canvas.setLineWidth(0.25)

    # 依頼日
    font_size = 11
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(380, 650, dt[0][2])

    # 発注先
    font_size = 12
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(20, 620, dt[0][46] + '　' + dt[0][6] + dt[0][7])
    pdf_canvas.line(20, 612, 175, 612) 

    # 自社情報
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)

    # ロゴ追加
    img = './mysite/myapp/templates/image/image1.jpg'
    #img = './static/image/image1.jpg'
    pdf_canvas.drawImage(img, 110*mm, 213*mm , 20*mm, 5*mm)

    pdf_canvas.drawString(375, 605, dt[0][31] + dt[0][32])
    pdf_canvas.drawString(310, 590, '〒 ' + dt[0][24])
    pdf_canvas.drawString(310, 580, dt[0][25] + dt[0][26] + dt[0][27] + dt[0][28])
    pdf_canvas.drawString(310, 570, 'TEL: ' + dt[0][29] + '　FAX: ' + dt[0][30])

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(20, 570,'下記の通りご依頼致します。')

    # line 
    pdf_canvas.line(20, 560, 480, 560) 
    pdf_canvas.line(250, 380, 250, 560) 

    # 原糸メーカー
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(25, 550,'原糸メーカー')
    pdf_canvas.drawString(80, 535, dt[0][47])
    # Line
    pdf_canvas.line(20, 530, 480, 530) 

    # 原糸出荷
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(25, 520,'原糸出荷')
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(80, 505, dt[0][44])
    # Line
    pdf_canvas.line(20, 500, 480, 500) 

    # 品番
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(25, 490,'品番')
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(80, 475, dt[0][5])
    # Line
    pdf_canvas.line(20, 470, 480, 470) 

    # 品名
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(25, 460,'品名')
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(80, 445, dt[0][3])
    # Line
    pdf_canvas.line(20, 440, 480, 440) 

    # 番手
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(25, 430,'番手')
    pdf_canvas.drawString(80, 415, dt[0][4])
    # Line
    pdf_canvas.line(20, 410, 480, 410) 

    # 混率
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(25, 400,'混率')
    pdf_canvas.drawString(80, 385, dt[0][42])

    # Line
    pdf_canvas.line(20, 380, 480, 380) 

    # オーダーNO
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(255, 550,'オーダーNO')

    font_size = 11
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(310, 535, dt[0][0] + '-' + dt[0][1])

    # アパレル
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(255, 490,'アパレル')
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(310, 475, dt[0][49])

    # 出荷先名
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(255, 460,'出荷先')
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(310, 445, dt[0][34])

    # 出荷先住所
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(255, 430, dt[0][35] + ' ' + dt[0][36] + dt[0][37] + dt[0][38] + dt[0][39])

    # 出荷先TEL
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(310, 415, 'TEL:' + dt[0][40])

    # 項番、色番、カラー、仕立、数量、摘要
    style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)
    itemNo0 = Paragraph('項番',style)
    itemNo1 = Paragraph('色番',style)
    itemNo2 = Paragraph('色' + '&nbsp' + '名',style)
    itemNo4 = Paragraph('数量',style)
    itemNo5 = Paragraph('単価',style)
    itemNo7 = Paragraph('希望納期',style)
    itemNo8 = Paragraph('回答納期',style)
    itemNo6 = Paragraph('備' + '&nbsp&nbsp&nbsp' + '考',style)

    data = [
        [itemNo0, itemNo1, itemNo2, itemNo4, itemNo5, itemNo7, itemNo8, itemNo6] ,
    ]

    table = Table(data, colWidths=(15*mm, 15*mm, 20*mm, 15*mm, 15*mm, 20*mm, 20*mm, 43*mm), rowHeights=9.0*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 9),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 120.0*mm)

    data =[]
    l=len(dt)
    total=0
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_RIGHT)
    styleCenter = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=8, alignment=TA_CENTER)

    for i in range(11):
        if i<l: 
            row = dt[i]
            total += Decimal(row[19])
            # 指定した列の左寄せ
            DetailColorNumber = Paragraph(row[16],styleLeft)
            DetailColor = Paragraph(row[17],styleLeft)
            #DetailTailoring = Paragraph(row[18],styleCenter)
            DetailSummary = Paragraph(row[21],styleLeft)
            # 指定した列の右寄せ
            DetailItemNumber = Paragraph(row[15],styleCenter)
            Volume = Paragraph(row[19],styleRight)
            DetailUnitPrice = Paragraph(row[20],styleRight)
            StainAnswerDeadline = Paragraph(row[45],styleCenter)
            SpecifyDeliveryDate = Paragraph(row[8],styleCenter)            
            data += [
                    [DetailItemNumber, DetailColorNumber, DetailColor, Volume, DetailUnitPrice, StainAnswerDeadline, SpecifyDeliveryDate, DetailSummary],
            ]
        else:
            if i==10:
                # 指定した列の右寄せ
                Detailtotal = Paragraph(str(total),styleRight)
                data += [
                        ['','　合　　計','',Detailtotal,'','',''],
                ]
            else:            
                data += [
                        ['','','','','','',''],
                ]

        table = Table(data, colWidths=(15*mm, 15*mm, 20*mm, 15*mm, 15*mm, 20*mm, 20*mm, 43*mm), rowHeights=9.0*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 8),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (8, 9), 0.25, colors.black),
                ('LINEABOVE', (0, 10), (8, 10), 0.25, colors.black),
                ('INNERGRID', (3, 10), (4, 10), 0.25, colors.black),
                ('INNERGRID', (2, 10), (3, 10), 0.25, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (1, 10), (2, 10), 5),
            ]))

    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 21.0*mm)

    # ロゴ追加
    img = './mysite/myapp/templates/image/image2.jpg'
    #img = './static/image/image2.jpg'
    pdf_canvas.drawImage(img, 65*mm, 5*mm, 38*mm, 7*mm)

    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()
