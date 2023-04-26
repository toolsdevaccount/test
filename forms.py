from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomerSupplier,OrderingTable,OrderingDetail

from django.forms import ModelChoiceField

# バリデーション
import re

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','is_superuser')

class ManagerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.first_name + obj.last_name

class CustomerSupplierForm(forms.ModelForm):
    ManagerCode = ManagerChoiceField(queryset=get_user_model().objects.all(),empty_label='')

    class Meta:
        model = CustomerSupplier
        fields = ('CustomerCode', 'CustomerName', 'CustomerOmitName', 'CustomerNameKana', 'Department','PostCode',
                  'PrefecturesCode','Municipalities','Address','BuildingName','PhoneNumber','FaxNumber','MasterDiv',
                  'ClosingDate','ExDepositMonth','ExDepositDate','ExDepositDiv','ManagerCode','OffsetDiv')   

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

class CustomerSupplierChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.CustomerCode + ":" + obj.CustomerOmitName

class OrderingForm(forms.ModelForm):
    DestinationCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    SupplierCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ShippingCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    CustomeCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    RequestCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')

    class Meta:
        model = OrderingTable
        fields = ('SlipDiv','OrderNumber','StartItemNumber','EndItemNumber','OrderingDate','StainShippingDate',
                  'ProductName','OrderingCount','StainPartNumber','StainMixRatio','DestinationCode','SupplierCode',
                  'ShippingCode','CustomeCode','RequestCode','SupplierPerson','TitleDiv','StockDiv','SpecifyDeliveryDate',
                  'StainAnswerDeadline','MarkName','OutputDiv',
                 )

    # オーダーナンバー重複チェック
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
            'DetailSellPrice','DetailPrice','DetailOverPrice','DetailSummary','AnswerDeadline','DeliveryManageDiv',
            ),
    extra=0,min_num=1,validate_min=True,can_delete=False
)
