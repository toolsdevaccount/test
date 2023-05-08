from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
import os
 
def make(request, filename="estimate"): # ファイル名
    if request.method == 'POST':
        pdf_canvas = set_info(filename) # キャンバス名
        print_string(pdf_canvas)
        pdf_canvas.save() # 保存

    return render(request, 'crud/pdftest/pdftest.html', {})

def set_info(filename):
    #file = "sample.pdf"
    file_path = os.path.expanduser("~") + "/Desktop/" + filename + ".pdf"
    pdf_canvas = canvas.Canvas(file_path.format(filename))

    #pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename))
    pdf_canvas.setAuthor("hpscript")
    pdf_canvas.setTitle("見積書")
    pdf_canvas.setSubject("見積書")
    return pdf_canvas
 
def print_string(pdf_canvas):
    # フォント登録
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
 
    width, height = A4
 
    # 見積日
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(440, 810, '見積日: 2020年10月1日')
 
    # title
    font_size = 24
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(245, 770, '御 見 積 書')
 
    # 線
    pdf_canvas.line(50, 750, 550, 750)
 
    # 宛先
    font_size = 14
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(60, 710, '六本木ソフトウェア株式会社　御中')
    pdf_canvas.drawString(60, 690, '営業部　 山田太郎 様')
 
    # 線
    pdf_canvas.line(50, 680, 350, 680)
 
    # 注釈
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(190, 670, '下記の通りお見積もり申し上げます。')
 
    # 納期、支払条件、有効期限
    font_size = 12
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(100, 635, '納期:')
    pdf_canvas.drawString(200, 635, '別途ご相談')
    pdf_canvas.line(200, 633, 350, 633)
 
    pdf_canvas.drawString(100, 615, '支払い条件:')
    pdf_canvas.drawString(200, 615, '月末締め翌月末払い')
    pdf_canvas.line(200, 612, 350, 612)
 
    pdf_canvas.drawString(100, 595, '有効期限:')
    pdf_canvas.drawString(200, 595, 'お見積り後2週間')
    pdf_canvas.line(200, 593, 350, 593)
 
    # 自社情報
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(360, 680, '丸の内ソフトウェア株式会社')
    pdf_canvas.drawString(360, 670, '〒100-0001')
    pdf_canvas.drawString(360, 660, '東京都千代田区千代田1-1-1')
    pdf_canvas.drawString(360, 645, 'TEL: 03-1234-5678')
    pdf_canvas.drawString(360, 635, 'E-mail: info@marunouchi-soft.com')
    pdf_canvas.drawString(360, 625, '担当: 田中一郎')
 
    # 合計金額
    font_size = 14
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(80, 550, '合計金額')
    pdf_canvas.drawString(180, 550, '800,000 円 (税込)')
 
    # 線
    pdf_canvas.line(50, 540, 350, 538)
 
    # 分類、型番、品名、規格寸法、基準単価
    data = [
        ['分類', '型番','品名', '規格寸法','数量','基準単価'],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' '],
    ]
    table = Table(data, colWidths=(25*mm, 25*mm, 55*mm, 25*mm, 15*mm,30*mm), rowHeights=7.5*mm)
    table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    # table.wrapOn(pdf_canvas, 20*mm, 20*mm)
    table.wrapOn(pdf_canvas, 20*mm, 20*mm)
    table.drawOn(pdf_canvas, 18*mm, 100*mm)
 
    # 小計、消費税、合計
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(360, 250, '小計:')
    pdf_canvas.drawString(450, 250, '700000円')
    pdf_canvas.line(360, 245, 550, 245) 
 
    pdf_canvas.drawString(360, 230, '消費税:')
    pdf_canvas.drawString(450, 230, '70000円')
    pdf_canvas.line(360, 225, 550, 225) 
 
    pdf_canvas.drawString(360, 210, '合計:')
    pdf_canvas.drawString(450, 210, '770000円')
    pdf_canvas.line(360, 205, 550, 207) 
 
    # 宛先
    font_size = 9
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(60, 175, '備考')
 
    pdf_canvas.rect(50, 50, 500, 120)
 
 
 
    pdf_canvas.showPage()
     
if __name__ == '__main__':
    make()
