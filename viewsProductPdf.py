from django.http import HttpResponse
from django.shortcuts import render,redirect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
# MySQL
import MySQLdb
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
        filename = "ProductOrder_" + strtime.strftime('%Y%m%d%H%M%S')
        make(pk,filename)
        #response = HttpResponse(open('./download/' + filename + '.pdf','rb').read(), content_type='application/pdf')
        response = HttpResponse(open('./mysite/download/' + filename + '.pdf','rb').read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        messages.error(request,message) 
        return redirect("myapp:productorderlist")
    return response

def make(pk,filename):
    dt = connect(pk)
    pdf_canvas = set_info(filename) # キャンバス名
    print_string(pdf_canvas,dt)
    pdf_canvas.save() # 保存

def set_info(filename):
    #pdf_canvas = canvas.Canvas("./download/{0}.pdf".format(filename),pagesize=landscape(A4))
    pdf_canvas = canvas.Canvas("./mysite/download/{0}.pdf".format(filename),pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("製品発注書")
    pdf_canvas.setSubject("製品発注書")
    return pdf_canvas

def connect(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
            ' SELECT ' 
                '  CAST(A.id AS CHAR),J.CustomerName, CASE WHEN A.ProductOrderTitleDiv=1 THEN "様" ELSE "御中" END ,A.ProductOrderSlipDiv,A.ProductOrderOrderNumber,A.ProductOrderPartNumber,IFNULL(DATE_FORMAT(A.ProductOrderOrderingDate,"%Y年%m月%d日"),"") '
                ' ,CAST(A.ProductOrderMerchandiseCode AS CHAR),B.CustomerName,IFNULL(DATE_FORMAT(A.ProductOrderDeliveryDate,"%Y年%m月%d日"),""),A.ProductOrderBrandName '
                ' ,FORMAT(C.McdUnitPrice,0),G.McdDtProductName,G.McdDtOrderingCount,G.McdDtStainMixRatio,FORMAT(G.McdDtlPrice,0),E.McdColorNumber '
                ' ,E.McdColor,F.McdSize,D.PodVolume,H.PostCode,H.CustomerName,I.prefecturename,H.Municipalities,H.Address,H.BuildingName,H.PhoneNumber,H.FaxNumber,H.EMAIL '
            ' FROM '
                ' myapp_productorder A LEFT JOIN myapp_customersupplier B on A.ProductOrderApparelCode_id = b.id '
                ' LEFT JOIN myapp_merchandise C on A.ProductOrderMerchandiseCode = C.id '
                ' LEFT JOIN	myapp_productorderdetail D on A.id = D.PodDetailId_id '
                ' LEFT JOIN myapp_merchandisecolor E on	D.PodColorId_id = E.id '
                ' LEFT JOIN myapp_merchandisesize F on D.PodSizeId_id = F.id '
                ' LEFT JOIN	myapp_customersupplier J on	A.ProductOrderDestinationCode_id = J.id '
                ' LEFT JOIN	myapp_merchandisedetail G on C.id = G.McdDtid_id '	
                ' ,(SELECT PostCode,CustomerName,PrefecturesCode_id,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber,EMAIL FROM myapp_customersupplier WHERE CustomerCode = "A00042") H '
                ' LEFT JOIN myapp_prefecture I on H.PrefecturesCode_id = I.id '
            ' WHERE '
                ' A.id = ' + str(pk)
            )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def print_string(pdf_canvas,dt):
    # フォント登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

    width, height = A4

    # 発注先
    font_size = 14
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 770, dt[0][1])
    pdf_canvas.drawString(200, 770, dt[0][2])
    pdf_canvas.line(20, 760, 240, 760) 

    # 発注日
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(450, 770, '発注日: ' + dt[0][6])

    # 発注番号
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(450, 750, '発注番号: ' + dt[0][0])

    # 自社情報
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(380, 720, dt[0][21])
    pdf_canvas.drawString(380, 700, '〒 ' + dt[0][20])
    pdf_canvas.drawString(380, 680, dt[0][22] + dt[0][23] + dt[0][24] + dt[0][25])
    pdf_canvas.drawString(380, 660, 'TEL: ' + dt[0][26] + '　FAX: ' + dt[0][27])
    pdf_canvas.drawString(380, 640, 'E-mail: ' + dt[0][28])

    # title
    font_size = 12
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(260, 620, '製 品 発 注 書')

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(150, 600,'下記の通り発注いたしますので、ご手配のほどよろしくお願い申し上げます')

    # line
    pdf_canvas.line(20, 590, 570, 590)  #上
    pdf_canvas.line(20, 590, 20, 500)   #左
    pdf_canvas.line(20, 500, 570, 500)  #下 
    pdf_canvas.line(570,590, 570, 500)  #右 
    pdf_canvas.line(120, 590, 120, 500) #中縦
    pdf_canvas.line(20, 560, 570, 560)  #中横
    pdf_canvas.line(20, 530, 570, 530)  #中横

    # オーダーNO
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 570,'オーダーNO')
    pdf_canvas.drawString(140,570, dt[0][3] + dt[0][4])
    pdf_canvas.line(210, 590, 210, 560) #中縦

    # アパレル
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 540,'アパレル')
    pdf_canvas.drawString(140,540, dt[0][8])

    # ブランド名
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 510,'ブランド')
    pdf_canvas.drawString(140,510, dt[0][10])

    # 
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 570,'オーダーNO')
    pdf_canvas.drawString(140,570, dt[0][3] + dt[0][4])
    pdf_canvas.line(210, 590, 210, 560) #中縦

    # 本品番
    font_size = 9
    pdf_canvas.line(300, 590, 300, 560) #中縦
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(240, 570,'本品番')
    pdf_canvas.drawString(320,570, dt[0][5])
    pdf_canvas.line(390, 590, 390, 500) #中縦

    # 商品コード
    font_size = 9
    pdf_canvas.line(470, 590, 470, 500) #中縦
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(400, 570,'商品コード')
    pdf_canvas.drawString(490,570, dt[0][7])

    # 納期
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(400, 540,'納期')
    pdf_canvas.drawString(490,540, dt[0][9])

    # 仕入単価
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(400, 510,'仕入単価')
    pdf_canvas.drawString(490, 510, dt[0][11])

    # 品名、番手、混率、単価、条件
    style = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=9, alignment=TA_CENTER)
    itemNo0 = Paragraph('品名',style)
    itemNo1 = Paragraph('番手',style)
    itemNo2 = Paragraph('混率',style)
    itemNo3 = Paragraph('単価',style)
    itemNo4 = Paragraph('条件',style)

    data = [
        [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4] ,
    ]

    table = Table(data, colWidths=(55*mm, 30*mm, 55*mm, 35*mm, 19*mm), rowHeights=7.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 9),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 160.0*mm)

    data =[]
    l=len(dt)
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=9, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=9, alignment=TA_RIGHT)

    for i in range(6):
        if i<l: 
            row = dt[i]
            #total += Decimal(row[19])
            # 指定した列の左寄せ
            ProductName = Paragraph(row[12],styleLeft)
            OrderingCount = Paragraph(row[13],styleLeft)
            StainMixRatio = Paragraph(row[14],styleLeft)
            # 指定した列の右寄せ
            DtlPrice = Paragraph(row[15],styleRight)
            data += [
                    [ProductName, OrderingCount, StainMixRatio, DtlPrice, ''],
            ]
        else:
            data += [
                    ['','','','',''],
            ]

        table = Table(data, colWidths=(55*mm, 30*mm, 55*mm, 35*mm, 19*mm), rowHeights=7.5*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 9),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 115.0*mm)

    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()
