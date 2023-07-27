from django.http import HttpResponse
from django.shortcuts import render,redirect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait, landscape
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
        filename = "PurchaseOrder_" + strtime.strftime('%Y%m%d%H%M%S')
        make(pk,filename)
        #response = HttpResponse(open('./download/' + filename + '.pdf','rb').read(), content_type='application/pdf')
        response = HttpResponse(open('./mysite/download/' + filename + '.pdf','rb').read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        messages.error(request,message) 
        return redirect("myapp:orderinglist")
    return response

def make(pk,filename):
    dt = connect(pk)
    if dt[0][43]==1:
        pdf_canvas = set_info(filename) # キャンバス名
        print_string(pdf_canvas,dt)
    if dt[0][43]==2 or dt[0][43]==3:
        pdf_canvas = set_info_stain(filename) # キャンバス名
        print_string_StainRequest(pdf_canvas,dt)
    pdf_canvas.save() # 保存

def set_info(filename):
    #pdf_canvas = canvas.Canvas("./download/{0}.pdf".format(filename),pagesize=landscape(A4))
    pdf_canvas = canvas.Canvas("./mysite/download/{0}.pdf".format(filename),pagesize=landscape(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("注文書")
    pdf_canvas.setSubject("注文書")
    return pdf_canvas

def set_info_stain(filename):
    #pdf_canvas = canvas.Canvas("./download/{0}.pdf".format(filename),pagesize=portrait(A4))
    pdf_canvas = canvas.Canvas("./mysite/download/{0}.pdf".format(filename),pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("染色依頼注文書")
    pdf_canvas.setSubject("染色依頼注文書")
    return pdf_canvas

def connect(pk):
    #conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
        ' SELECT '
                '  a.SlipDiv,a.OrderNumber,IFNULL(DATE_FORMAT(a.OrderingDate,"%Y年%m月%d日"),""),a.ProductName,a.OrderingCount,a.StainPartNumber,a.SupplierPerson'
                ' ,CASE WHEN a.TitleDiv=1 THEN "様" ELSE "御中" END'
                ' ,IFNULL(DATE_FORMAT(b.StainAnswerDeadline,"%Y年%m月%d日"),""),c.CustomerName,c.PostCode,h.prefecturename,c.Municipalities,c.Address'
                ' ,c.BuildingName,b.DetailItemNumber,b.DetailColorNumber,b.DetailColor,b.DetailTailoring,FORMAT(b.DetailVolume,2),FORMAT(b.detailunitprice,0)'
                ' ,b.detailsummary,"",e.CustomerName,e.PostCode,g.prefecturename,e.Municipalities,e.Address'
                ' ,e.BuildingName,e.PhoneNumber,e.FaxNumber,d.first_name,d.last_name,d.email,f.CustomerName,f.PostCode,i.prefecturename,f.Municipalities'
                ' ,f.Address,f.BuildingName,f.PhoneNumber,f.FaxNumber,a.StainMixRatio,a.OutputDiv'
                ' ,IFNULL(DATE_FORMAT(a.StainShippingDate,"%Y年%m月%d日"),""),IFNULL(DATE_FORMAT(b.SpecifyDeliveryDate,"%Y年%m月%d日"),"")'
        ' FROM '
                'myapp_orderingtable a '
        ' LEFT JOIN myapp_orderingdetail b on a.id = b.OrderingTableId_id'
        ' LEFT JOIN myapp_customersupplier c on a.RequestCode_id = c.id'
        ' LEFT JOIN auth_user d on c.ManagerCode = d.id'
        ' LEFT JOIN myapp_customersupplier f on a.ShippingCode_id = f.id'
        ' LEFT JOIN myapp_prefecture h on c.PrefecturesCode_id = h.id'
        ' LEFT JOIN myapp_prefecture i on f.PrefecturesCode_id = i.id'
        ' ,(SELECT PostCode,CustomerName,PrefecturesCode_id,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber FROM myapp_customersupplier WHERE CustomerCode = "A00042" AND is_Deleted = 0) e'
        ' LEFT JOIN myapp_prefecture g on e.PrefecturesCode_id = g.id'
        ' WHERE a.id = ' + str(pk) + ' AND b.is_Deleted= 0' 
        ' ORDER BY b.DetailItemNumber ASC' 
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

    # 注文日
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(700, 550, '注文日: ' + dt[0][2])

    # title
    font_size = 24
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(350, 550, '注　文　書')

    # 発注先
    font_size = 11
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 550, dt[0][9] + '　' + dt[0][6] + '　' + dt[0][7])

    # 出荷先
    font_size = 10
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 430, '出荷先: ' + dt[0][34])
    pdf_canvas.drawString(50, 410, '〒 ' + dt[0][35])
    pdf_canvas.drawString(50, 390, dt[0][36] + dt[0][37] + dt[0][38] + dt[0][39])
    #pdf_canvas.drawString(50, 370, 'TEL: ' + dt[0][40] + '　FAX: ' + dt[0][41])
    pdf_canvas.drawString(50, 370, 'TEL: ' + dt[0][40])

    # 自社情報
    font_size = 10
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(590, 490, dt[0][23] + '　' + dt[0][31] + dt[0][32])
    pdf_canvas.drawString(590, 470, '〒 ' + dt[0][24])
    pdf_canvas.drawString(590, 450, dt[0][25] + dt[0][26] + dt[0][27] + dt[0][28])
    pdf_canvas.drawString(590, 430, 'TEL: ' + dt[0][29] + '　FAX: ' + dt[0][30])
    pdf_canvas.drawString(590, 410, 'E-mail: ' + dt[0][33])

    # 発注番号
    font_size = 11
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(685, 370, '発注番号: ' + dt[0][0] + dt[0][1])
    pdf_canvas.line(680, 365, 808, 365) 

    # 品名、番手、色番、色名、数量、単位、単価、希望納期、回答納期、備考(中央寄せ)
    style = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=8, alignment=TA_CENTER)
    itemNo0 = Paragraph('品名',style)
    itemNo1 = Paragraph('番手',style)
    itemNo2 = Paragraph('色番',style)
    itemNo3 = Paragraph('色名',style)
    itemNo4 = Paragraph('数量',style)
    itemNo5 = Paragraph('単位',style)
    itemNo6 = Paragraph('単価',style)
    itemNo7 = Paragraph('希望納期',style)
    itemNo8 = Paragraph('回答納期',style)
    itemNo9 = Paragraph('備考',style)

    data = [
        [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4, itemNo5, itemNo6, itemNo7, itemNo8, itemNo9],
    ]

    table = Table(data, colWidths=(40*mm, 15*mm, 20*mm, 40*mm, 20*mm, 15*mm, 20*mm, 30*mm, 30*mm, 40*mm), rowHeights=7.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 10*mm, 10*mm)
    table.drawOn(pdf_canvas, 15*mm, 118.0*mm)

    data =[]
    l=len(dt)
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=8, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=8, alignment=TA_RIGHT)

    for i in range(9):
        if i<l: 
            row = dt[i]
            # 指定した列の左寄せ
            ProductName = Paragraph(row[3],styleLeft)
            OrderingCount = Paragraph(row[4],styleLeft)
            DetailColorNumber = Paragraph(row[16],styleLeft)
            DetailColor = Paragraph(row[17],styleLeft)
            DetailSummary = Paragraph(row[21],styleLeft)
            # 指定した列の右寄せ
            Volume = Paragraph(row[19],styleRight)
            UnitPrice = Paragraph(row[20],styleRight)
            StainAnswerDeadline = Paragraph(row[8],styleRight)
            SpecifyDeliveryDate = Paragraph(row[45],styleRight)

            data += [
                    [ProductName, OrderingCount, DetailColorNumber, DetailColor, Volume, ' ', UnitPrice, SpecifyDeliveryDate, StainAnswerDeadline, DetailSummary],
            ]
        else:
            data += [
                    ['','','','','','','','','',''],
            ]

        table = Table(data, colWidths=(40*mm, 15*mm, 20*mm, 40*mm, 20*mm, 15*mm, 20*mm, 30*mm, 30*mm, 40*mm), rowHeights=7.5*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 8),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

    table.wrapOn(pdf_canvas, 10*mm, 10*mm)
    table.drawOn(pdf_canvas, 15*mm, 50.5*mm)

    # 摘要
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 100, '摘要')

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 80, '※単価の違いがございましたらお手数ですがご連絡ください。')

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 60, '　出荷次第、納品書を翌日当社宛に発注番号を必ずご記入の上、ご一報ください。')

    pdf_canvas.rect(43, 20, 765, 100) 
 
    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()

def print_string_StainRequest(pdf_canvas,dt):
    # フォント登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

    width, height = A4

    # title
    font_size = 20
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    if dt[0][43]==2:
        pdf_canvas.drawString(240, 800, '染 付 依 頼 書')
    if dt[0][43]==3:
        pdf_canvas.drawString(180, 800, 'ビ ー カ ー 染 付 依 頼 書')

    # 発注番号
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(450, 790, '発注番号: ' + dt[0][0] + dt[0][1])
    #pdf_canvas.line(680, 365, 808, 365) 

    # 依頼日
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(450, 770, '依頼日: ' + dt[0][2])

    # 発注先
    font_size = 14
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 770, dt[0][9] + '　' + dt[0][6] + '　' + dt[0][7])
    pdf_canvas.line(20, 760, 240, 760) 

    # 自社情報
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(380, 720, dt[0][23] + '　' + dt[0][31] + dt[0][32])
    pdf_canvas.drawString(380, 700, '〒 ' + dt[0][24])
    pdf_canvas.drawString(380, 680, dt[0][25] + dt[0][26] + dt[0][27] + dt[0][28])
    pdf_canvas.drawString(380, 660, 'TEL: ' + dt[0][29] + '　FAX: ' + dt[0][30])
    pdf_canvas.drawString(380, 640, 'E-mail: ' + dt[0][33])

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 620,'下 記 の 通 り 依 頼 い た し ま す 。')

    # line
    pdf_canvas.line(20, 610, 570, 610) 
    pdf_canvas.line(290, 430, 290, 610) 

    # 原糸メーカー
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 590,'原糸メーカー')
    pdf_canvas.line(20, 580, 570, 580) 

    # 原糸出荷
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 560,'原糸出荷')
    pdf_canvas.line(20, 550, 570, 550) 
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(90, 560, dt[0][44])

    # 品番
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 530,'品番')
    pdf_canvas.line(20, 520, 570, 520) 
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(90, 530, dt[0][5])

    # 品名
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 500,'品名')
    pdf_canvas.line(20, 490, 570, 490) 
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(90, 500, dt[0][3])

    # 番手
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 470,'番手')
    pdf_canvas.line(20, 460, 570, 460) 
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(90, 470, dt[0][4])

    # 混率
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20, 440,'混率')
    pdf_canvas.line(20, 430, 570, 430) 
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(90, 440, dt[0][42])

    # 希望納期
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(300, 590,'希望納期')
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(370, 590, dt[0][8])

    # 回答納期
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(300, 560,'回答納期')
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(370, 560, dt[0][45])

    # 不明
    #font_size = 9
    #pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    #pdf_canvas.drawString(300, 550,'')

    # 仕入単価
    #font_size = 9
    #pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    #pdf_canvas.drawString(300, 530,'仕入単価')
    #pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    #pdf_canvas.drawString(370, 530, dt[0][20])

    # 出荷先名
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(300, 530,'出荷先名')
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(370, 530, dt[0][34])

    # 項番、色番、カラー、仕立、数量、摘要
    style = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=9, alignment=TA_CENTER)
    itemNo0 = Paragraph('項番',style)
    itemNo1 = Paragraph('色番',style)
    itemNo2 = Paragraph('カラー',style)
    itemNo3 = Paragraph('仕立',style)
    itemNo4 = Paragraph('数量',style)
    itemNo5 = Paragraph('単価',style)
    itemNo6 = Paragraph('摘要',style)

    data = [
        [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4, itemNo5, itemNo6] ,
    ]

    table = Table(data, colWidths=(20*mm, 30*mm, 30*mm, 15*mm, 20*mm, 20*mm, 60*mm), rowHeights=7.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 9),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 133.0*mm)

    data =[]
    l=len(dt)
    total=0
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=9, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiKakuGo-W5', fontSize=9, alignment=TA_RIGHT)

    for i in range(15):
        if i<l: 
            row = dt[i]
            total += Decimal(row[19])
            # 指定した列の左寄せ
            DetailColorNumber = Paragraph(row[16],styleLeft)
            DetailColor = Paragraph(row[17],styleLeft)
            DetailTailoring = Paragraph(row[18],styleLeft)
            DetailSummary = Paragraph(row[21],styleLeft)
            # 指定した列の右寄せ
            DetailItemNumber = Paragraph(row[15],styleRight)
            Volume = Paragraph(row[19],styleRight)
            DetailUnitPrice = Paragraph(row[20],styleRight)
            data += [
                    [DetailItemNumber, DetailColorNumber, DetailColor, DetailTailoring, Volume, DetailUnitPrice, DetailSummary],
            ]
        else:
            if i==14:
                # 指定した列の右寄せ
                Detailtotal = Paragraph(str(total),styleRight)
                data += [
                        ['','','','',Detailtotal,''],
                ]
            else:            
                data += [
                        ['','','','','',''],
                ]

        table = Table(data, colWidths=(20*mm, 30*mm, 30*mm, 15*mm, 20*mm, 20*mm, 60*mm), rowHeights=7.5*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 9),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 20.5*mm)

    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()
