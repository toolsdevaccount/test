from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import prefecture, CustomerSupplier, OrderingTable, OrderingDetail

from django.forms import ModelChoiceField
# バリデーション
import re
# 検索機能のために追加
from django.db.models import Q

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','is_superuser')

class ManagerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.first_name + obj.last_name

class PrefectureChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.prefecturename

class CustomerSupplierForm(forms.ModelForm):
    ManagerCode = ManagerChoiceField(queryset=get_user_model().objects.all(),empty_label='')
    PrefecturesCode = PrefectureChoiceField(queryset=prefecture.objects.all(),empty_label='')

    class Meta:
        model = CustomerSupplier
        fields = ('CustomerCode', 'CustomerName', 'CustomerOmitName', 'CustomerNameKana', 'Department','PostCode',
                  'PrefecturesCode','Municipalities','Address','BuildingName','PhoneNumber','FaxNumber','MasterDiv',
                  'ClosingDate','ExDepositMonth','ExDepositDate','ExDepositDiv','ManagerCode','OffsetDiv','EMAIL',
                  'LastClaimBalance','LastReceivable','LastPayable','LastProceeds','ProceedsTarget')   

    # 得意先仕入先コード
    def clean_CustomerCode(self):
        code = self.cleaned_data['CustomerCode']
        if code:
            if not re.match(r'^[A-Z]', code):
                raise forms.ValidationError(u'コードの先頭は英大文字で')
        return code

    # 郵便番号
    def clean_PostCode(self):
        zip = self.cleaned_data['PostCode']
        if zip:
            if not re.match(r'^\d{3}-\d{4}$', zip):
                raise forms.ValidationError(u'郵便番号はXXX-XXXXの形式で')
        return zip

    # 電話番号
    def clean_PhoneNumber(self):
        tel = self.cleaned_data['PhoneNumber']
        if tel:
            if not re.match(r'^\d{2,4}-\d{2,4}-\d{4}$', tel):
                raise forms.ValidationError(u'電話番号はXXXX-XXXX-XXXXの形式で')
        return tel

    # FAX番号
    def clean_FaxNumber(self):
        tel = self.cleaned_data['FaxNumber']
        if tel:
            if not re.match(r'^\d{2,4}-\d{2,4}-\d{4}$', tel):
                raise forms.ValidationError(u'FAX番号はXXXX-XXXX-XXXXの形式で')
        return tel

    # E-MAIL
    #def clean_EMAIL(self):
    #    email = self.cleaned_data['EMAIL']
    #    if email:
    #        if not re.match(r'^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$', email):
    #            raise forms.ValidationError(u'EMAILはXXXX@XXXX.XX.XXの形式で')
    #    return email

class CustomerSupplierChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        #return  obj.CustomerOmitName[0:5] + ":" + obj.CustomerCode
        return  obj.CustomerCode + ":" + obj.CustomerOmitName[0:5]

class OrderingForm(forms.ModelForm):
    class Meta:
        model = OrderingTable
        fields = ('SlipDiv','OrderNumber','OrderingDate','StainShippingDate','ProductName','OrderingCount','StainPartNumber',
                  'StainMixRatio','DestinationCode','SupplierCode','ShippingCode','CustomeCode','StainShippingCode','RequestCode','SupplierPerson',
                  'TitleDiv','StockDiv','MarkName','OutputDiv','SampleDiv',
                 )

    # 手配先
    def clean_DestinationCode(self):
        DestinationCode = self.cleaned_data['DestinationCode']
        if DestinationCode == None:
            raise forms.ValidationError(u'このフィールドは必須です。')
        return DestinationCode

    # オーダーナンバー重複チェック
    #def clean_OrderNumber(self):
    #    SlipDiv = self.cleaned_data['SlipDiv']
    #    OrderNumber = self.cleaned_data['OrderNumber']
    #    idcnt = OrderingTable.objects.filter(id__exact = self.instance.pk).count()
    #    OrderNumbercnt = OrderingTable.objects.filter(OrderNumber__exact = OrderNumber.zfill(7)).count()
    #    if idcnt > 0:
    #        OrderNumbercnt = 0           
    #    if OrderNumbercnt > 0 and (SlipDiv == "S" or SlipDiv == "B" or SlipDiv == "F" or SlipDiv == "D"):
    #        OrderNumbercnt = 0
    #    if OrderNumber:
    #        if OrderNumbercnt > 0:
    #            raise forms.ValidationError(u'オーダーNOが重複しています')
    #    return OrderNumber

    #def clean(self):
    #    cleaned_data = super(OrderingForm, self).clean()
    #    try:            
    #        orderNo = OrderingTable.objects.filter(
    #            SlipDiv = self.cleaned_data['SlipDiv'],
    #            OrderNumber = self.cleaned_data['OrderNumber'].zfill(7),
    #            StartItemNumber = self.cleaned_data['StartItemNumber'].zfill(4),
    #            EndItemNumber = self.cleaned_data['StartItemNumber'].zfill(4),
    #        ).exists()
    #    except KeyError:
    #        raise forms.ValidationError(u'登録できません。')
    #    if orderNo:
    #        raise forms.ValidationError('このオーダーNOは既に登録済みです。')
    #    return cleaned_data
    
OrderingFormset = forms.inlineformset_factory(
    OrderingTable, OrderingDetail, 
    fields=('DetailItemNumber','DetailColorNumber','DetailColor','DetailTailoring','DetailVolume','DetailUnitPrice',
            'DetailSellPrice','DetailPrice','DetailOverPrice','DetailSummary','SpecifyDeliveryDate','StainAnswerDeadline',
            'DeliveryManageDiv','PrintDiv',
            ),
    extra=0,min_num=1,validate_min=True,can_delete=True
)
