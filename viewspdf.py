from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
import os
import MySQLdb
 
def make(request, filename="estimate"): # ファイル名
    if request.method == 'POST':
        pdf_canvas = set_info(filename) # キャンバス名
        dt = connect()
        print_string(pdf_canvas,dt)
        pdf_canvas.save() # 保存

    return render(request, 'crud/pdftest/pdftest.html', {})

def set_info(filename):
    #file = "sample.pdf"
    file_path = os.path.expanduser("~") + "/Desktop/" + filename + ".pdf"
    pdf_canvas = canvas.Canvas(file_path.format(filename),pagesize=landscape(A4))

    #pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("注文書")
    pdf_canvas.setSubject("注文書")
    return pdf_canvas

def connect():
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    cur = conn.cursor()
    sql = (' SELECT a.SlipDiv,a.OrderNumber,DATE_FORMAT(a.OrderingDate,"%Y年%m月%d日"),a.ProductName,a.OrderingCount,a.StainPartNumber,a.SupplierPerson	,a.titlediv'
           ' ,DATE_FORMAT(a.StainAnswerDeadline,"%Y年%m月%d日"),c.CustomerName,c.PostCode,c.PrefecturesCode,c.Municipalities,c.Address,c.BuildingName,b.DetailItemNumber'
           ' ,b.DetailColorNumber,b.DetailColor,b.DetailTailoring,FORMAT(b.DetailVolume,2),FORMAT(b.detailunitprice,0),b.detailsummary'
           ' ,DATE_FORMAT(b.AnswerDeadline,"%Y年%m月%d日"),e.CustomerName,e.PostCode,e.PrefecturesCode,e.Municipalities,e.Address,e.BuildingName'
           ' ,e.PhoneNumber,e.FaxNumber,d.first_name,d.last_name,d.email'
           ' ,f.CustomerName,f.PostCode,f.PrefecturesCode,f.Municipalities,f.Address,f.BuildingName,f.PhoneNumber,f.FaxNumber'
           ' FROM myapp_orderingtable a LEFT JOIN myapp_orderingdetail b on a.id = b.OrderingTableId_id	LEFT JOIN myapp_customersupplier c on a.SupplierCode_id = c.id'
           ' LEFT JOIN auth_user d on c.ManagerCode = d.id'
           ' LEFT JOIN  myapp_customersupplier f on  a.ShippingCode_id = f.id'
           ' ,(SELECT PostCode,CustomerName,PrefecturesCode,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber FROM myapp_customersupplier WHERE CustomerCode = "A00042") e'
           ' WHERE a.SlipDiv="A" AND a.OrderNumber="0350306" AND a.OutputDiv=1 AND b.is_Deleted= 0' )
    try:
        cur.execute(sql)
        result = cur.fetchall()
        #for result in cur.fetchall():
        #    print(result)
        
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
    pdf_canvas.drawString(30, 550, dt[0][9] + '　' + dt[0][6] + '　' + '様')

    # 出荷先
    font_size = 10
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 430, '出荷先: ' + dt[0][34])
    pdf_canvas.drawString(50, 410, '〒 ' + dt[0][35])
    pdf_canvas.drawString(50, 390, dt[0][37] + dt[0][38] + dt[0][39])
    pdf_canvas.drawString(50, 370, 'TEL: ' + dt[0][40] + '　FAX: ' + dt[0][41])

    # 自社情報
    font_size = 10
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(590, 490, dt[0][23] + '　' + dt[0][31] + dt[0][32])
    pdf_canvas.drawString(590, 470, '〒 ' + dt[0][24])
    pdf_canvas.drawString(590, 450, dt[0][26] + dt[0][27] + dt[0][28])
    pdf_canvas.drawString(590, 430, 'TEL: ' + dt[0][29] + '　FAX: ' + dt[0][30])
    pdf_canvas.drawString(590, 410, 'E-mail: ' + dt[0][33])

    # 発注番号
    font_size = 11
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(650, 370, '発注番号: ' + dt[0][0] + dt[0][1])
    #pdf_canvas.line(360, 245, 550, 245) 

    #for row in dt:  
    # 品名、番手、色番、色名、数量、単位、単価、希望納期、回答納期、備考
    data = [
        ['品名', '番手','色番', '色名','数量','単位','単価','希望納期','回答納期','備考'],
        [dt[0][3],dt[0][4],dt[0][16],dt[0][17],dt[0][19],' ',dt[0][20],dt[0][8],dt[0][22],' '],
        [dt[1][3],dt[1][4],dt[1][16],dt[1][17],dt[1][19],' ',dt[1][20],dt[1][8],dt[1][22],' '],
        [dt[2][3],dt[2][4],dt[2][16],dt[2][17],dt[2][19],' ',dt[2][20],dt[2][8],dt[2][22],' '],
        [dt[3][3],dt[3][4],dt[3][16],dt[3][17],dt[3][19],' ',dt[3][20],dt[3][8],dt[3][22],' '],
        [dt[4][3],dt[4][4],dt[4][16],dt[4][17],dt[4][19],' ',dt[4][20],dt[4][8],dt[4][22],' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ]

    table = Table(data, colWidths=(40*mm, 15*mm, 20*mm, 40*mm, 20*mm, 15*mm, 20*mm, 30*mm, 30*mm, 40*mm), rowHeights=7.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    #table.wrapOn(pdf_canvas, 20*mm, 20*mm)
    #table.drawOn(pdf_canvas, 18*mm, 100*mm)
    table.wrapOn(pdf_canvas, 10*mm, 10*mm)
    table.drawOn(pdf_canvas, 15*mm, 50*mm)

    # 摘要
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(50, 100, '摘要')

    pdf_canvas.rect(43, 20, 765, 100) 
 
    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()
