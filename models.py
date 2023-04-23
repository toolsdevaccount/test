from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
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

    PrefecturesCode = [
            (0, ""),
        (1,"北海道"),
        (2,"青森県"),
        (3,"岩手県"),
        (4,"宮城県"),
        (5,"秋田県"),
        (6,"山形県"),
        (7,"福島県"),
        (8,"茨城県"),
        (9,"栃木県"),
        (10,"群馬県"),
        (11,"埼玉県"),
        (12,"千葉県"),
        (13,"東京都"),
        (14,"神奈川県"),
        (15,"新潟県"),
        (16,"富山県"),
        (17,"石川県"),
        (18,"福井県"),
        (19,"山梨県"),
        (20,"長野県"),
        (21,"岐阜県"),
        (22,"静岡県"),
        (23,"愛知県"),
        (24,"三重県"),
        (25,"滋賀県"),
        (26,"京都府"),
        (27,"大阪府"),
        (28,"兵庫県"),
        (29,"奈良県"),
        (30,"和歌山県"),
        (31,"鳥取県"),
        (32,"島根県"),
        (33,"岡山県"),
        (34,"広島県"),
        (35,"山口県"),
        (36,"徳島県"),
        (37,"香川県"),
        (38,"愛媛県"),
        (39,"高知県"),
        (40,"福岡県"),
        (41,"佐賀県"),
        (42,"長崎県"),
        (43,"熊本県"),
        (44,"大分県"),
        (45,"宮崎県"),
        (46,"鹿児島県"),
        (47,"沖縄県"),
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
    CustomerCode = models.CharField(max_length=8,null=False,verbose_name="コード")
    CustomerName = models.CharField(max_length=30,null=False,blank=True,verbose_name="名称")
    CustomerOmitName = models.CharField(max_length=12,null=False,blank=True,verbose_name="略称")
    CustomerNameKana = models.CharField(max_length=30,null=False,blank=True,verbose_name="カナ")
    Department = models.CharField(max_length=20,null=False,blank=True,default="",verbose_name="部署名")
    PostCode = models.CharField(max_length=8,null=False,blank=True,verbose_name="郵便番号")
    PrefecturesCode = models.IntegerField(default=0,null=False,choices=PrefecturesCode,verbose_name="都道府県コード")
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
    Created_at = models.DateTimeField(null=False, blank=False,default='2000-01-01 00:00:00',verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default='2000-01-01 00:00:00',verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return self.CustomerCode
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
    StartItemNumber = models.CharField(max_length=4,null=False,blank=False,default=0,verbose_name="開始項番")
    EndItemNumber = models.CharField(max_length=4,null=False,blank=False,default=0,verbose_name="終了項番")
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
    SupplierPerson = models.CharField(max_length=30,null=False,blank=True,verbose_name="仕入先担当者名")
    TitleDiv = models.IntegerField(null=False,blank=True,default=0,choices=Title,verbose_name="敬称区分")
    StockDiv = models.BooleanField(null=False,blank=False,default=False,verbose_name="在庫済区分")
    SpecifyDeliveryDate = models.DateField(null=True,blank=True,default="2000-01-01",verbose_name="指定納期")
    StainAnswerDeadline = models.DateField(null=True,blank=True,default="2000-01-01",verbose_name="回答納期")
    MarkName = models.CharField(max_length=20,null=False,blank=True,verbose_name="マーク名")
    OutputDiv = models.IntegerField(null=False,blank=True,default=0,choices=Output,verbose_name="出力区分")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default='2000-01-01 00:00:00',verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default='2000-01-01 00:00:00',verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    # ユニーク制約（以下の組み合わせを一意とする）
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["SlipDiv", "OrderNumber", "StartItemNumber", "EndItemNumber"],
                name="ordernumber_unique"
            ),
        ]  
   
    def __str__(self):
        return self.ProductName
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/ordering/orderinglist.html')

class OrderingDetail(models.Model):
    OrderingTableId = models.ForeignKey(OrderingTable,on_delete=models.PROTECT,blank=True, null=True,related_name='OrderingTableId',verbose_name="受発注テーブルid")
    DetailItemNumber = models.CharField(max_length=4,null=False,blank=False,default=0,verbose_name="項番")
    DetailColorNumber = models.CharField(max_length=6,null=False,blank=True,default=0,verbose_name="色番")
    DetailColor = models.CharField(max_length=12,null=False,blank=True,default=0,verbose_name="カラー")
    DetailTailoring = models.CharField(max_length=11,null=False,blank=True,default=0,verbose_name="仕立")
    DetailVolume = models.DecimalField(max_digits=8,decimal_places=2, null=False,blank=True,default=0.00,verbose_name="数量")
    DetailUnitPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=True,default=0,verbose_name="仕入単価")
    DetailPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=True,default=0,verbose_name="通常単価")
    DetailOverPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=True,default=0,verbose_name="UP分単価")
    DetailSellPrice = models.DecimalField(max_digits=8,decimal_places=0, null=False,blank=True,default=0,verbose_name="販売単価")
    DetailSummary = models.TextField(max_length=1000,null=False,blank=True,verbose_name="摘要")
    AnswerDeadline = models.DateField(null=True,blank=True,verbose_name="納期回答")
    DeliveryManageDiv = models.BooleanField(null=False,blank=False,default=False,verbose_name="納期管理済区分")
    Created_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="登録者id")
    Updated_id = models.BigIntegerField(null=False,blank=True,default=0,verbose_name="更新者id")
    Created_at = models.DateTimeField(null=False, blank=False,default='2000-01-01 00:00:00',verbose_name="登録日時")
    Updated_at = models.DateTimeField(null=False, blank=False,default='2000-01-01 00:00:00',verbose_name="更新日時")
    is_Deleted = models.BooleanField(null=False,blank=False,default=False,verbose_name="削除区分")

    def __str__(self):
        return self.DetailItemNumber
    # 新規登録・編集完了後のリダイレクト先
    def get_absolute_url(self):
        return reverse('crud/ordering/orderinglist.html')