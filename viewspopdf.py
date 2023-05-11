from django.http import HttpResponse
from django.shortcuts import render,redirect
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
# MySQL
import MySQLdb
# 日時
from django.utils import timezone
import datetime

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
 
def pdf(request,pk):
    strtime = timezone.now() + datetime.timedelta(hours=9)
    filename = "estimate_" + strtime.strftime('%Y%m%d%H%M%S')
    make(pk,filename)
    response = HttpResponse(open('./download/' + filename + '.pdf','rb').read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'

    return response

def make(pk,filename):
    pdf_canvas = set_info(filename) # キャンバス名
    dt = connect(pk)
    print_string(pdf_canvas,dt)
    pdf_canvas.save() # 保存

def set_info(filename):
    pdf_canvas = canvas.Canvas("./download/{0}.pdf".format(filename),pagesize=landscape(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("注文書")
    pdf_canvas.setSubject("注文書")
    return pdf_canvas

def connect(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    cur = conn.cursor()
    sql = (' SELECT '
                '  a.SlipDiv,a.OrderNumber,DATE_FORMAT(a.OrderingDate,"%Y年%m月%d日"),a.ProductName,a.OrderingCount,a.StainPartNumber,a.SupplierPerson'
                ' ,j.titledivname,DATE_FORMAT(a.StainAnswerDeadline,"%Y年%m月%d日"),c.CustomerName,c.PostCode,h.prefecturename,c.Municipalities,c.Address'
                ' ,c.BuildingName,b.DetailItemNumber,b.DetailColorNumber,b.DetailColor,b.DetailTailoring,FORMAT(b.DetailVolume,2),FORMAT(b.detailunitprice,0)'
                ' ,b.detailsummary,DATE_FORMAT(b.AnswerDeadline,"%Y年%m月%d日"),e.CustomerName,e.PostCode,g.prefecturename,e.Municipalities,e.Address'
                ' ,e.BuildingName,e.PhoneNumber,e.FaxNumber,d.first_name,d.last_name,d.email,f.CustomerName,f.PostCode,i.prefecturename,f.Municipalities'
                ' ,f.Address,f.BuildingName,f.PhoneNumber,f.FaxNumber'
           ' FROM '
                'myapp_orderingtable a '
           ' LEFT JOIN myapp_orderingdetail b on a.id = b.OrderingTableId_id'
           ' LEFT JOIN myapp_customersupplier c on a.SupplierCode_id = c.id'
           ' LEFT JOIN auth_user d on c.ManagerCode = d.id'
           ' LEFT JOIN myapp_customersupplier f on  a.ShippingCode_id = f.id'
           ' LEFT JOIN prefecture h on c.PrefecturesCode = h.prefecturecode'
           ' LEFT JOIN prefecture i on f.PrefecturesCode = i.prefecturecode'
           ' LEFT JOIN title j on a.titlediv = j.titledivcode'
           ' ,(SELECT PostCode,CustomerName,PrefecturesCode,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber FROM myapp_customersupplier WHERE CustomerCode = "A00042") e'
	       ' LEFT JOIN prefecture g on e.PrefecturesCode = g.prefecturecode'
           ' WHERE a.id = ' + str(pk) + ' AND a.OutputDiv=1 AND b.is_Deleted= 0' 
        )
    try:
        cur.execute(sql)
        result = cur.fetchall()
        
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)

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
    pdf_canvas.drawString(50, 370, 'TEL: ' + dt[0][40] + '　FAX: ' + dt[0][41])

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
            # 指定した列の右寄せ
            Volume = Paragraph(row[19],styleRight)
            UnitPrice = Paragraph(row[20],styleRight)
            StainAnswerDeadline = Paragraph(row[8],styleRight)
            AnswerDeadline = Paragraph(row[22],styleRight)

            data += [
                    [ProductName, OrderingCount, DetailColorNumber, DetailColor, Volume, ' ', UnitPrice, StainAnswerDeadline, AnswerDeadline, ' '],
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
