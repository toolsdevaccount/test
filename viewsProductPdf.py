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
# イメージファイル
from PIL import Image
# 文字列折り返し
import textwrap

def pdf(request,pk):
    try:
        strtime = timezone.now() + datetime.timedelta(hours=9)
        filename = "ProductOrder_" + strtime.strftime('%Y%m%d%H%M%S')
        response = HttpResponse(status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
        make(pk,response)
        UpdateQuery(pk)
    except Exception as e:
        message = "PDF作成時にエラーが発生しました"
        messages.error(request,message) 
        return redirect("myapp:productorderlist")
    return response

def make(pk,response):
    dt = connect(pk)
    dtsize = getsize(pk)
    dtcolor = getcolor(pk)
    dtimage = getimage(pk)
    pdf_canvas = set_info(response) # キャンバス名
    print_string(pdf_canvas,dt,dtsize,dtcolor,dtimage)
    pdf_canvas.save() # 保存

def set_info(response):
    pdf_canvas = canvas.Canvas(response,pagesize=portrait(A4))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("製品発注書")
    pdf_canvas.setSubject("製品発注書")
    return pdf_canvas

def UpdateQuery(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
           ' UPDATE ' 
	           ' myapp_productorder '
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
            '    CAST(A.id AS CHAR)'
            '   ,J.CustomerName'
            '   ,CASE WHEN A.ProductOrderTitleDiv=1 THEN "様" ELSE "御中" END '
            '   ,A.ProductOrderSlipDiv '
            '   ,A.ProductOrderOrderNumber' 
            '   ,A.ProductOrderPartNumber '
            '   ,IFNULL(DATE_FORMAT(A.ProductOrderOrderingDate,"%Y年%m月%d日"),"") '
            '   ,CAST(A.ProductOrderMerchandiseCode AS CHAR) '
            '   ,B.CustomerName,IFNULL(DATE_FORMAT(A.ProductOrderDeliveryDate,"%Y年%m月%d日"),"") '
            '   ,A.ProductOrderBrandName '
            '   ,FORMAT(C.McdUnitPrice,0) '
            '   ,G.McdDtProductName '
            '   ,G.McdDtOrderingCount '
            '   ,G.McdDtStainMixRatio '
            '   ,FORMAT(G.McdDtlPrice,0) '
            '   ,H.PostCode '
            '   ,H.CustomerName ' 
            '   ,I.prefecturename '
            '   ,H.Municipalities '
            '   ,H.Address '
            '   ,H.BuildingName '
            '   ,H.PhoneNumber '
            '   ,H.FaxNumber '
            '   ,H.EMAIL '
            '   ,A.ProductOrderSupplierPerson '
            '   ,k.first_name '
            '   ,k.last_name '
            '   ,CASE C.McdUnitcode '
            '       WHEN 1 THEN "￥" '
            '                WHEN 2 THEN "US$" '
            '                WHEN 3 THEN "US$" '
            '                WHEN 4 THEN "US$" '
            '                WHEN 5 THEN "US$" '
            '                WHEN 6 THEN "US$" '
            '                WHEN 7 THEN "US$" '
            '       ELSE "" '
            '   END '
            '   ,CASE C.McdUnitcode '
            '       WHEN 1 THEN "" '
            '       WHEN 2 THEN "　FOB東京" '
            '       WHEN 3 THEN "　FOB上海" '
            '       WHEN 4 THEN "　CIF東京" '
            '       WHEN 5 THEN "　CIF上海" '
            '       WHEN 6 THEN "　CMT東京" '
            '       WHEN 7 THEN "　CMT上海" '
            '       ELSE "" '
            '   END '
            '   ,CASE G.McdDtUnitCode '
            '       WHEN 1 THEN "￥" '
            '       WHEN 2 THEN "US$" '
            '       WHEN 3 THEN "US$" '
            '       WHEN 4 THEN "US$" '
            '       WHEN 5 THEN "US$" '
            '       WHEN 6 THEN "US$" '
            '       WHEN 7 THEN "US$" '
            '       ELSE "" '
            '   END '
            '   ,CASE G.McdDtUnitCode '
            '       WHEN 1 THEN "" '
            '       WHEN 2 THEN "FOB東京" '
            '       WHEN 3 THEN "FOB上海" '
            '       WHEN 4 THEN "CIF東京" '
            '       WHEN 5 THEN "CIF上海" '
            '       WHEN 6 THEN "CMT東京" '
            '       WHEN 7 THEN "CMT上海" '
            '       ELSE "" '
            '   END '
            ' FROM '
            '   myapp_productorder A '
            '   LEFT JOIN ' 
            '   auth_user k on '
            '       A.ManagerCode = k.id'
            '   LEFT JOIN '
            '   myapp_customersupplier B on '
            '       A.ProductOrderApparelCode_id = b.id '
            '   LEFT JOIN '
            '   myapp_merchandise C on '
            '       A.ProductOrderMerchandiseCode = C.id '
            '   LEFT JOIN '
            '  	myapp_customersupplier J on	'
            '      A.ProductOrderDestinationCode_id = J.id '
            '   LEFT JOIN '
            '   myapp_merchandisedetail G on '
            '       C.id = G.McdDtid_id '	
            '   ,(SELECT PostCode,CustomerName,PrefecturesCode_id,Municipalities,Address,BuildingName,PhoneNumber,FaxNumber,EMAIL FROM myapp_customersupplier WHERE CustomerCode = "A00042" AND is_Deleted = 0) H '
            '   LEFT JOIN '
            '   myapp_prefecture I on '
            '       H.PrefecturesCode_id = I.id '
            ' WHERE '
                ' A.id = ' + str(pk)
            )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def getsize(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
                ' SELECT '
                ' 	 B.McdSize '
                ' FROM '
                '	myapp_productorder A '
                '	LEFT JOIN '
                '	myapp_merchandisesize B on '
                '		A.ProductOrderMerchandiseCode = B.McdSizeId_id '
                ' WHERE '
                '   A.id = ' + str(pk)
            )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def getcolor(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
            ' select '
            '	  color '
            '    ,group_concat(size order by size) key_list ' 
            '    ,group_concat(max_value order by size) value_list '
            '    ,colorNumber '
            ' from '
            ' ( '
            '  SELECT '
            '	 a.id			    AS id '
            '	,b.McdColor			AS color '
            '	,c.McdSize			AS size ' 
            '	,max(a.PodVolume) 	AS max_value '
            '  	,b.McdColorNumber	AS colorNumber '
            '  FROM '
            '	myapp_productorderdetail a '
            '	left join '
            '	myapp_merchandisecolor b on '
            '		a.PodColorId_id = b.id '
            '	left join '
            '	myapp_merchandisesize c on '
            '		a.PodsizeId_id = c.id '
            ' WHERE '
            '	a.PodDetailId_id = ' + str(pk) +
            '  GROUP BY ' 
            '	b.McdColor, c.McdSize, b.McdColorNumber'
            ' ) t '
            ' group by' 
            '	 color '
            '   ,colorNumber'
            ' order by'
            '    t.id '
            )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def getimage(pk):
    conn = MySQLdb.connect(user='root',passwd='PWStools', host='127.0.0.1',db='ksmdb',port=3308)
    #conn = MySQLdb.connect(user='test',passwd='password', host='127.0.0.1',db='DjangoSample',port=3308)
    cur = conn.cursor()
    sql = (
            ' SELECT ' 
            '    A.ProductOrderMarkName '
            '   ,A.ProductOrderSummary '
            '   ,B.McdTempPartNumber ' 
            '	,IFNULL(C.uploadPath,"") ' 
            ' FROM ' 
            '	myapp_productorder A '
            '   LEFT JOIN '
            '   myapp_merchandise B ON '
            '       A.ProductOrderMerchandiseCode = B.id '
			'	LEFT JOIN ' 
          	'	myapp_merchandisefileupload C ON '
            '		A.id = C.McdDtuploadid_id '
            ' WHERE '
            '     A.id = ' + str(pk) +
            ' AND B.is_Deleted = 0 ' 
            )
    cur.execute(sql)
    result = cur.fetchall()     

    cur.close()
    conn.close()

    return result

def print_string(pdf_canvas,dt,dtsize,dtcolor,dtimage):
    # フォント登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    width, height = A4

    # 線の太さ
    pdf_canvas.setLineWidth(0.25)

    # 発注先
    font_size = 12
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(20, 790, dt[0][1] + '　' + dt[0][25] + dt[0][2])

    # 発注日
    font_size = 11
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(480, 820, dt[0][6])

    # 発注番号
    font_size = 10
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(480, 800, 'No' + dt[0][0])

    # 自社情報
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)

    # ロゴ追加
    #img = './mysite/myapp/templates/image/image1.jpg'
    img = './static/image/image1.jpg'
    pdf_canvas.drawImage(img, 145*mm, 261*mm , 20*mm, 5*mm)

    pdf_canvas.drawString(470, 740, dt[0][26] + dt[0][27])
    pdf_canvas.drawString(410, 730, '〒 ' + dt[0][16])
    pdf_canvas.drawString(410, 720, dt[0][18] + dt[0][19] + dt[0][20] + dt[0][21])
    pdf_canvas.drawString(410, 710, 'TEL: ' + dt[0][22] + '　FAX: ' + dt[0][23])

    # title
    font_size = 16
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(260, 690, '製品発注書')

    # メッセージ
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(150, 660,'下記の通り発注いたしますので、御手配のほどよろしくお願い申し上げます')

    # line
    pdf_canvas.line(20, 650, 570, 650)  #上
    pdf_canvas.line(20, 650, 20, 590)   #左
    pdf_canvas.line(20, 590, 570, 590)  #下 
    pdf_canvas.line(570,650, 570, 590)  #右 
    pdf_canvas.line(120, 650, 120, 590) #中縦
    pdf_canvas.line(20, 630, 570, 630)  #中横
    pdf_canvas.line(20, 610, 570, 610)  #中横

    # オーダーNO
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(50, 635,'オーダーNO')
    pdf_canvas.drawString(130,635, dt[0][3] + dt[0][4])
    pdf_canvas.line(210, 650, 210, 630) #中縦

    # アパレル
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(50, 615,'アパレル')
    pdf_canvas.drawString(130,615, dt[0][8])

    # ブランド名
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(50, 595,'ブランド')
    pdf_canvas.drawString(130,595, dt[0][10])

    # 本品番
    font_size = 9
    pdf_canvas.line(300, 650, 300, 630) #中縦
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(240, 635,'本品番')
    pdf_canvas.drawString(310,635, dt[0][5])
    pdf_canvas.line(390, 650, 390, 590) #中縦

    # 商品コード
    font_size = 9
    pdf_canvas.line(470, 650, 470, 590) #中縦
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(400, 635,'商品コード')
    pdf_canvas.drawString(480, 635, dt[0][7])

    # 納期
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(400, 615,'納期')
    pdf_canvas.drawString(480, 615, dt[0][9])

    # 仕入単価
    font_size = 9
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(400, 595,'仕入単価')
    pdf_canvas.drawString(480, 595, dt[0][28] + dt[0][11] + dt[0][29])

    # 品名、番手、混率、単価、条件
    style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)
    itemNo0 = Paragraph('品名',style)
    itemNo1 = Paragraph('番手',style)
    itemNo2 = Paragraph('混率',style)
    itemNo3 = Paragraph('単価',style)
    itemNo4 = Paragraph('条件',style)

    data = [
        [itemNo0, itemNo1, itemNo2, itemNo3, itemNo4] ,
    ]

    table = Table(data, colWidths=(55*mm, 30*mm, 55*mm, 35*mm, 19*mm), rowHeights=6.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 9),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 198.0*mm)

    data =[]
    l=len(dt)
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_RIGHT)

    for i in range(6):
        if i<l: 
            row = dt[i]
            # 指定した列の左寄せ
            ProductName = Paragraph(row[12],styleLeft)
            OrderingCount = Paragraph(row[13],styleLeft)
            StainMixRatio = Paragraph(row[14],styleLeft)
            UnitDiv = Paragraph(row[31],styleLeft)
            # 指定した列の右寄せ
            DtlPrice = Paragraph(row[30] + row[15],styleRight)
            data += [
                    [ProductName, OrderingCount, StainMixRatio, DtlPrice, UnitDiv],
            ]
        else:
            data += [
                    ['','','','',''],
            ]

        table = Table(data, colWidths=(55*mm, 30*mm, 55*mm, 35*mm, 19*mm), rowHeights=6.5*mm)
        table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 9),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))

    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 159.0*mm)

    # サイズ
    data =[]
    l=len(dtsize)

    style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)
    titleNo0 = Paragraph('色番',style)
    titleNo1 = Paragraph('カラー/サイズ',style)
    titleNo8 = Paragraph('合　計',style)

    for i in range(6):
        if i<l: 
            row = dtsize[i]
            if i==0:
                titleNo2 = Paragraph(row[0],style)
            if i==1:
                titleNo3 = Paragraph(row[0],style)
            if i==2:
                titleNo4 = Paragraph(row[0],style)
            if i==3:
                titleNo5 = Paragraph(row[0],style)
            if i==4:
                titleNo6 = Paragraph(row[0],style)
            if i==5:
                titleNo7 = Paragraph(row[0],style)
        else:
            if i==0:
                titleNo2 = ''
            if i==1:
                titleNo3 = ''
            if i==2:
                titleNo4 = ''
            if i==3:
                titleNo5 = ''
            if i==4:
                titleNo6 = ''
            if i==5:
                titleNo7 = ''

    data = [
        [titleNo0, titleNo1, titleNo2, titleNo3, titleNo4, titleNo5, titleNo6, titleNo7, titleNo8] ,
    ]

    table = Table(data, colWidths=(15*mm, 39*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm), rowHeights=6.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 9),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 150.0*mm)

    # カラー
    data =[]
    l=len(dtcolor)
    total = 0
    itemNo12total = 0
    itemNo13total = 0
    itemNo14total = 0
    itemNo15total = 0
    itemNo16total = 0
    itemNo17total = 0

    style = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_CENTER)
    styleLeft = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_LEFT)
    styleRight = ParagraphStyle(name='Normal', fontName='HeiseiMin-W3', fontSize=9, alignment=TA_RIGHT)

    for i in range(12):
        if i<l:
            row = dtcolor[i]
            itemNo11 = Paragraph(row[0],styleLeft)
            item = row[2]
            itemNo10 = row[3]
            Vol = item.split(',')
            col = len(Vol)
            itemNo12 = ""
            itemNo13 = ""
            itemNo14 = ""
            itemNo15 = ""
            itemNo16 = ""
            itemNo13 = ""
            itemNo14 = ""
            itemNo15 = ""
            itemNo16 = ""
            itemNo17 = ""
            total = 0
            for k in range(col):
                if k==0:   
                    itemNo12 = Paragraph(f"{int(Vol[0]):,}",styleRight)
                    total += Decimal(Vol[0])
                    itemNo12total += Decimal(Vol[0])
                if k==1:   
                    itemNo13 = Paragraph(f"{int(Vol[1]):,}",styleRight)
                    total += Decimal(Vol[1])
                    itemNo13total += Decimal(Vol[1])
                if k==2:   
                    itemNo14 = Paragraph(f"{int(Vol[2]):,}",styleRight)
                    total += Decimal(Vol[2])
                    itemNo14total += Decimal(Vol[2])
                if k==3:   
                    itemNo15 = Paragraph(f"{int(Vol[3]):,}",styleRight)
                    total += Decimal(Vol[3])
                    itemNo15total += Decimal(Vol[3])
                if k==4:   
                    itemNo16 = Paragraph(f"{int(Vol[4]):,}",styleRight)
                    total += Decimal(Vol[4])
                    itemNo16total += Decimal(Vol[4])
                if k==5:   
                    itemNo17 = Paragraph(f"{int(Vol[5]):,}",styleRight)
                    total += Decimal(Vol[5])
                    itemNo17total += Decimal(Vol[5])
            detailtotal = Paragraph(f"{int(total):,}",styleRight)
            data += [
                [itemNo10, itemNo11,itemNo12,itemNo13,itemNo14,itemNo15,itemNo16,itemNo17,detailtotal] ,
            ]
        else:
            if i==11:
                # 総合計の計算
                itemtotal = Decimal(itemNo12total) + Decimal(itemNo13total) + Decimal(itemNo14total) + Decimal(itemNo15total) + Decimal(itemNo16total) + Decimal(itemNo17total)
                itemtotal = Paragraph(f"{int(itemtotal):,}",styleRight)
                # 指定した列の右寄せ
                if Decimal(itemNo12total) != 0:
                    itemNo12total = Paragraph(f"{int(itemNo12total):,}",styleRight)
                else:
                    itemNo12total = ''

                if Decimal(itemNo13total) != 0:
                    itemNo13total = Paragraph(f"{int(itemNo13total):,}",styleRight)
                else:
                    itemNo13total = ''

                if Decimal(itemNo14total) != 0:
                    itemNo14total = Paragraph(f"{int(itemNo14total):,}",styleRight)
                else:
                    itemNo14total = ''

                if Decimal(itemNo15total) != 0:
                    itemNo15total = Paragraph(f"{int(itemNo15total):,}",styleRight)
                else:
                    itemNo15total = ''

                if Decimal(itemNo16total) != 0:
                    itemNo16total = Paragraph(f"{int(itemNo16total):,}",styleRight)
                else:
                    itemNo16total = ''

                if Decimal(itemNo17total) != 0:
                    itemNo17total = Paragraph(f"{int(itemNo17total):,}",styleRight)
                else:
                    itemNo17total = ''

                data += [
                    ['', Paragraph('合計',style),itemNo12total,itemNo13total,itemNo14total,itemNo15total,itemNo16total,itemNo17total ,itemtotal] ,
                ]
            else:
                data += [
                    ['', '','','','','','','',''] ,
                ]

    table = Table(data, colWidths=(15*mm, 39*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm, 20*mm), rowHeights=6.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiMin-W3', 9),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
    table.wrapOn(pdf_canvas, 7*mm, 10*mm)
    table.drawOn(pdf_canvas, 7*mm, 72*mm)

    # イメージ(画像ファイルを挿入)
    l=len(dtimage)

    for i in range(l):
        row = dtimage[i]
        if row[3]!="":
            #img = './mysite/media/' + row[3]
            img = './media/' + row[3]
            if i==0:
                pdf_canvas.drawImage(img, 11*mm, 28*mm , 25*mm, 25*mm)
            if i==1:
                pdf_canvas.drawImage(img, 30*mm, 28*mm , 25*mm, 25*mm)

    if l > 0:
        # 仮品番
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(25, 170,'[仮品番]:')
        pdf_canvas.drawString(80 ,170, dtimage[0][2])

        # マーク名
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(200, 170,'[マーク名]:')
        pdf_canvas.drawString(280, 170, dtimage[0][0])

        # 備考
        font_size = 9
        pdf_canvas.setFont('HeiseiMin-W3', font_size)
        pdf_canvas.drawString(25, 160,'[備考]:')
        pdf_canvas.drawString(80, 160, textwrap.fill(dtimage[0][1], 12, max_lines=2, placeholder=' ~',))

    # 
    font_size = 14
    pdf_canvas.setFont('HeiseiMin-W3', font_size)
    pdf_canvas.drawString(350, 105,'Signature')
    pdf_canvas.line(350, 100, 520, 100) 

    pdf_canvas.rect(20, 70, 550, 120) 

    # ロゴ追加
    #img = './mysite/myapp/templates/image/image2.jpg'
    img = './static/image/image2.jpg'
    pdf_canvas.drawImage(img, 85*mm, 10*mm, 38*mm, 7*mm)

    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()
