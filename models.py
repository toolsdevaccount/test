from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# 日時
from django.utils import timezone
import datetime
# イメージリサイズ
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import os

# Create your models here.
class prefecture(models.Model):
    prefecturecode = models.CharField(max_length=2,null=False,blank=True,verbose_name="都道府県コード")
    prefecturename = models.CharField(max_length=255,null=False,blank=True,verbose_name="都道府県名")
    blockname = models.CharField(max_length=255,null=False,blank=True,verbose_name="地域名称")

    def __str__(self):
        return str(self.prefecturecode)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/customersupplier/customersupplierlist.html')

class CustomerSupplier(models.Model):
    Closing = [
            (0, ""),
            (5, "5日"),
            (10, "10日"),
            (15, "15日"),
            (20, "20日"),
            (25, "25日"),
            (31, "末日"),
        ]
   
    MasterDiv = [
            (0, ""),
            (1, "得意先/仕入先未使用"),
            (2, "得意先"),
            (3, "仕入先"),
            (4, "得意先/仕入先使用"),
        ]
    
    Offset = [
            (0, ""),
            (1, "相殺する"),
            (2, "相殺しない"),
        ]

    ExDepositDiv = [
            (0, ""),
            (1, "現金"),
            (2, "現金以外"),
        ]

    ExDepositMonth = [
            (0, ""),
            (1, "1ヶ月"),
            (2, "2ヶ月"),
            (3, "3ヶ月"),
            (4, "4ヶ月"),
            (5, "5ヶ月"),
            (6, "6ヶ月"),
            (99, "6ヶ月以上"),
        ]

    CustomerCode = models.CharField(max_length=6,null=False,verbose_name="コード")
    CustomerName = models.CharField(max_length=30,null=False,blank=True,verbose_name="名称")
    CustomerOmitName = models.CharField(max_length=12,null=False,blank=True,verbose_name="略称")
    CustomerNameKana = models.CharField(max_length=30,null=False,blank=True,verbose_name="カナ")
    Department = models.CharField(max_length=20,null=False,blank=True,default="",verbose_name="部署名")
    PostCode = models.CharField(max_length=8,null=False,blank=True,verbose_name="郵便番号")
    #PrefecturesCode = models.IntegerField(default=0,null=False,choices=prefecture,verbose_name="都道府県コード")
    PrefecturesCode = models.ForeignKey(prefecture,on_delete=models.PROTECT,related_name='PrefecturesCode',null=False,default=1,verbose_name="都道府県コード")
    Municipalities = models.CharField(max_length=24,null=False,blank=True,verbose_name="市区町村")
    Address = models.CharField(max_length=24,null=False,blank=True,verbose_name="番地")
    BuildingName = models.CharField(max_length=24,null=False,blank=True,verbose_name="建物名")
    PhoneNumber = models.CharField(max_length=12,null=False,blank=True,verbose_name="電話番号")
    FaxNumber = models.CharField(max_length=12,null=False,blank=True,verbose_name="FAX番号")
    EMAIL = models.EmailField(null=False,blank=True,verbose_name="メールアドレス")
    MasterDiv = models.IntegerField(null=False,default=0,choices=MasterDiv,verbose_name="マスタ区分")
    ClosingDate = models.IntegerField(null=False,default=0,choices=Closing,verbose_name="締日")
    ExDepositMonth = models.IntegerField(null=False,default=0,choices=ExDepositMonth,verbose_name="入金予定月")
    ExDepositDate = models.IntegerField(null=False,default=0,choices=Closing,verbose_name="入金予定日")
    ExDepositDiv = models.IntegerField(null=False,default=0,choices=ExDepositDiv,verbose_name="入金予定区分")
    ManagerCode = models.ForeignKey(User, to_field='id',on_delete=models.SET_NULL, null=True, db_column='ManagerCode',verbose_name="担当者コード")
    OffsetDiv = models.IntegerField(null=False,default=0,choices=Offset,verbose_name="相殺出力区分")
    LastClaimBalance = models.DecimalField(max_digits=10,decimal_places=0,default=0,null=False,blank=True,verbose_name="前回請求残")
    LastReceivable= models.DecimalField(max_digits=10,decimal_places=0,default=0,null=False,blank=True,verbose_name="前月売掛残")
    LastPayable = models.DecimalField(max_digits=10,decimal_places=0,default=0,null=False,blank=True,verbose_name="前月買掛残")
    LastProceeds = models.DecimalField(max_digits=10,decimal_places=0,default=0,null=False,blank=True,verbose_name="前年売上実績")
    ProceedsTarget = models.DecimalField(max_digits=10,decimal_places=0,default=0,null=False,blank=True,verbose_name="当年売上目標")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.CustomerCode)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/customersupplier/customersupplierlist.html')

class OrderingTable(models.Model):
    Output = [
            (0, ""),
            (1, "通常"),
            (2, "染色"),
            (3, "ビーカー染色"),
            (9, "その他"),
        ]
    Title = [
            (0, ""),
            (1, "様"),
            (2, "御中"),
    ]

    SlipDiv = models.CharField(max_length=1,null=False,blank=False,verbose_name="伝票区分")
    OrderNumber = models.CharField(max_length=7,null=False,blank=False,default=0,verbose_name="オーダーNO")
    OrderingDate = models.DateField(null=False,blank=False,default="2000-01-01",verbose_name="依頼日")
    StainShippingDate = models.DateField(null=True,blank=True,default="2000-01-01",verbose_name="原糸出荷日")
    ProductName = models.CharField(max_length=24,null=False,blank=True,verbose_name="商品名")
    OrderingCount = models.CharField(max_length=8,null=False,blank=True,verbose_name="番手")
    StainPartNumber = models.CharField(max_length=10,null=False,blank=True,verbose_name="品番")
    StainMixRatio = models.CharField(max_length=20,null=False,blank=True,verbose_name="混率")
    DestinationCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='DestinationCode',null=False,blank=True,verbose_name="手配先コード",default=1)
    SupplierCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='SupplierCode',verbose_name="仕入先コード")
    ShippingCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ShippingCode',verbose_name="出荷先コード")
    CustomeCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='CustomeCode',verbose_name="得意先コード")
    RequestCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='RequestCode',verbose_name="依頼先コード")
    StainShippingCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='StainShippingCode',verbose_name="原糸メーカーコード")
    SupplierPerson = models.CharField(max_length=30,null=False,blank=True,verbose_name="仕入先担当者名")
    TitleDiv = models.IntegerField(null=False,blank=True,default=0,choices=Title,verbose_name="敬称区分")
    StockDiv = models.BooleanField(null=False,blank=False,default=False,verbose_name="在庫済区分")
    MarkName = models.CharField(max_length=20,null=False,blank=True,verbose_name="マーク名")
    OutputDiv = models.IntegerField(null=False,blank=True,default=0,choices=Output,verbose_name="出力区分")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    # ユニーク制約（以下の組み合わせを一意とする）
    #class Meta:
    #    constraints = [
    #        models.UniqueConstraint(
    #            fields=["SlipDiv", "OrderNumber", "StartItemNumber", "EndItemNumber"],
    #            name="ordernumber_unique"
    #        ),
    #    ]  
   
    def __str__(self):
        return str(self.OrderNumber)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/ordering/orderinglist.html')

class OrderingDetail(models.Model):
    OrderingTableId = models.ForeignKey(OrderingTable,on_delete=models.PROTECT,blank=True, null=True,related_name='OrderingTableId',verbose_name="受発注テーブルid")
    DetailItemNumber = models.CharField(max_length=4,null=False,blank=False,default=0,verbose_name="項番")
    DetailColorNumber = models.CharField(max_length=6,null=False,blank=True,default=0,verbose_name="色番")
    DetailColor = models.CharField(max_length=12,null=False,blank=True,default=0,verbose_name="カラー")
    DetailTailoring = models.CharField(max_length=1,null=False,blank=True,default=0,verbose_name="仕立")
    DetailVolume = models.DecimalField(max_digits=8,decimal_places=2, null=False,blank=False,default=0.00,verbose_name="数量")
    DetailUnitPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="仕入単価")
    DetailPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="通常単価")
    DetailOverPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="UP分単価")
    DetailSellPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="販売単価")
    DetailSummary = models.TextField(max_length=1000,null=False,blank=True,verbose_name="摘要")
    SpecifyDeliveryDate = models.DateField(null=True,blank=True,default="2000-01-01",verbose_name="希望納期")
    StainAnswerDeadline = models.DateField(null=True,blank=True,default="2000-01-01",verbose_name="回答納期")
    DeliveryManageDiv = models.BooleanField(null=False,blank=False,default=False,verbose_name="納期管理済区分")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.DetailItemNumber)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/ordering/orderinglist.html')
    
class Merchandise(models.Model):
    MerchandiseTreatment = [
            (0, ""),
            (1, "通常"),
            (2, "扱停止"),
        ]
    MerchandiseUnitCode = [
        (0, ""),
        (1, "￥"),
        (2, "US$ FOB東京"),
        (3, "US$ FOB上海"),
        (4, "US$ CIF東京"),
        (5, "US$ CIF上海"),
        (6, "US$ CMT東京"),
        (7, "US$ CMT上海"),
        ]
    #McdCode = models.IntegerField(null=False,default=0,verbose_name="商品コード")
    McdTreatmentCode = models.IntegerField(null=False,blank=True,default=0,choices=MerchandiseTreatment,verbose_name="扱区分")
    McdPartNumber = models.CharField(max_length=20,null=False,blank=False,default=0,verbose_name="本品番")
    McdManagerCode = models.ForeignKey(User, to_field='id',on_delete=models.SET_NULL, null=True, db_column='ManagerCode',verbose_name="担当者コード")
    McdUnitPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="仕入単価")
    McdUnitCode = models.IntegerField(null=False,blank=True,default=0,choices=MerchandiseUnitCode,verbose_name="仕入単位")
    McdSellPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="販売単価")
    McdProcessfee = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=False,default=0,verbose_name="加工賃")
    McdProcessCode = models.IntegerField(null=False,blank=True,default=0,choices=MerchandiseUnitCode,verbose_name="加工賃単位")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.McdPartNumber)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/merchandise/merchandiselist.html')

class MerchandiseColor(models.Model):
    McdColorId = models.ForeignKey(Merchandise,on_delete=models.PROTECT,blank=True, null=True,related_name='McdColorId',verbose_name="商品マスタid")
    McdColor = models.CharField(max_length=20,null=False,blank=False,default=0,verbose_name="商品カラー")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.McdColor)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/merchandise/merchandiselist.html')

class MerchandiseSize(models.Model):
    McdSizeId = models.ForeignKey(Merchandise,on_delete=models.PROTECT,blank=True, null=True,related_name='McdSizeId',verbose_name="商品マスタid")
    McdSize = models.CharField(max_length=20,null=False,blank=False,default=0,verbose_name="商品サイズ")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.McdSize)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/merchandise/merchandiselist.html')

class MerchandiseDetail(models.Model):
    UnitCode = [
        (0, ""),
        (1, "￥"),
        (2, "US$ FOB東京"),
        (3, "US$ FOB上海"),
        (4, "US$ CIF東京"),
        (5, "US$ CIF上海"),
        (6, "US$ CMT東京"),
        (7, "US$ CMT上海"),
    ]  
    McdDtid = models.ForeignKey(Merchandise,on_delete=models.PROTECT,blank=True, null=True,related_name='McdDtid',verbose_name="商品マスタid")
    McdDtProductName = models.CharField(max_length=24,null=False,blank=True,verbose_name="品名")
    McdDtOrderingCount = models.CharField(max_length=8,null=False,blank=True,verbose_name="番手")
    McdDtStainMixRatio = models.CharField(max_length=20,null=False,blank=True,verbose_name="混率")
    McdDtlPrice = models.DecimalField(max_digits=8,decimal_places=2, null=False,blank=False,default=0.00,verbose_name="単価")
    McdDtUnitCode = models.IntegerField(null=False,blank=True,default=0,choices=UnitCode,verbose_name="単位")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.McdDtid)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/merchandise/merchandiselist.html')

class MerchandiseFileUpload(models.Model):
    McdDtuploadid = models.ForeignKey(Merchandise, on_delete=models.PROTECT, blank=True, null=True, related_name='McdDtuploadid', verbose_name="商品マスタid")
    uploadPath = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True, null=True, verbose_name="アップロードファイルパス")
    middle = ImageSpecField(source='uploadPath', processors=[ResizeToFill(600, 400)],  format="JPEG",  options={'quality': 75})  
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.McdDtuploadid)
    
    def file_name(self):
        return os.path.basename(self.uploadPath.name)

    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/merchandise/merchandiselist.html')

class ProductOrder(models.Model):
    ProductOrderTitleDiv = [
            (0, ""),
            (1, "様"),
            (2, "御中"),
        ]
    ProductOrderMerchandiseCode = models.IntegerField(null=False,default=0,verbose_name="商品コード")
    ProductOrderOrderingDate = models.DateField(null=False,blank=False,default="2000-01-01",verbose_name="発注日")
    ProductOrderManagerCode = models.ForeignKey(User, to_field='id',on_delete=models.SET_NULL, null=True, db_column='ManagerCode',verbose_name="担当者コード")
    ProductOrderSlipDiv = models.CharField(max_length=1,null=False,blank=False,verbose_name="伝票区分")
    ProductOrderOrderNumber = models.CharField(max_length=7,null=False,blank=False,default=0,verbose_name="オーダーNO")
    ProductOrderPartNumber = models.CharField(max_length=20,null=False,blank=False,default=0,verbose_name="本品番")
    ProductOrderApparelCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ProductOrderApparelCode',verbose_name="アパレルコード")
    ProductOrderDestinationCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ProductOrderDestinationCode',null=False,blank=True,verbose_name="手配先コード",default=1)
    ProductOrderSupplierCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ProductOrderSupplierCode',verbose_name="仕入先コード")
    ProductOrderSupplierPerson = models.CharField(max_length=30,null=False,blank=True,verbose_name="仕入先担当者名")
    ProductOrderTitleDiv = models.IntegerField(null=False,blank=True,default=0,choices=ProductOrderTitleDiv,verbose_name="敬称区分")
    ProductOrderShippingCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ProductOrderShippingCode',verbose_name="出荷先コード")
    ProductOrderCustomeCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ProductOrderCustomeCode',verbose_name="得意先コード")
    ProductOrderRequestCode = models.ForeignKey(CustomerSupplier,on_delete=models.PROTECT,related_name='ProductOrderRequestCode',verbose_name="依頼先コード")
    ProductOrderDeliveryDate = models.DateField(null=True,blank=True,default="2000-01-01",verbose_name="納期")
    ProductOrderBrandName = models.CharField(max_length=50,null=False,blank=True,default="",verbose_name="ブランド名")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.ProductOrderMerchandiseCode)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/productorder/productorderlist.html')

class ProductOrderDetail(models.Model):
    PodDetailId = models.ForeignKey(ProductOrder,on_delete=models.PROTECT,blank=True, null=True,related_name='PodDetailId',verbose_name="製品受発注明細id")
    PodColorId = models.ForeignKey(MerchandiseColor,on_delete=models.PROTECT,blank=True, null=True,related_name='PodColorId',verbose_name="商品カラーid")
    PodSizeId = models.ForeignKey(MerchandiseSize,on_delete=models.PROTECT,blank=True, null=True,related_name='PodSizeId',verbose_name="商品サイズid")
    PodVolume = models.DecimalField(max_digits=8, decimal_places=0, null=False, blank=False, default=0, verbose_name="数量")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default=timezone.now() + datetime.timedelta(hours=9),verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return str(self.PodDetailId)
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/productorder/productorderlist.html')
