from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.forms import UserCreationForm
from .models import ProductOrder, ProductOrderDetail, CustomerSupplier

from django.forms import ModelChoiceField
from datetime import datetime

# バリデーション
import re

User = get_user_model()

class ManagerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.first_name + obj.last_name

class CustomerSupplierChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.CustomerCode + ":" + obj.CustomerOmitName

class ProductOrderForm(forms.ModelForm):
    ProductOrderManagerCode = ManagerChoiceField(queryset=get_user_model().objects.all(),empty_label='')
    ProductOrderApparelCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderDestinationCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderSupplierCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderShippingCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderCustomeCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderRequestCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')

    class Meta:
        model = ProductOrder
        fields = ('ProductOrderMerchandiseCode', 'ProductOrderOrderingDate', 'ProductOrderManagerCode','ProductOrderSlipDiv', 'ProductOrderOrderNumber',
                  'ProductOrderPartNumber','ProductOrderApparelCode','ProductOrderDestinationCode','ProductOrderSupplierCode','ProductOrderShippingCode','ProductOrderCustomeCode',
                  'ProductOrderRequestCode','ProductOrderDeliveryDate','ProductOrderBrandName','ProductOrderSupplierPerson','ProductOrderTitleDiv',
                  )   

class ProductOrderDetailForm(forms.ModelForm):
    class Meta:
        model = ProductOrderDetail
        fields = ('PodColorId','PodSizeId','PodVolume',)


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
   
#OrderingFormset = forms.inlineformset_factory(
    #OrderingTable, OrderingDetail, 
    #fields=('DetailItemNumber','DetailColorNumber','DetailColor','DetailTailoring','DetailVolume','DetailUnitPrice',
    #        'DetailSellPrice','DetailPrice','DetailOverPrice','DetailSummary','SpecifyDeliveryDate','StainAnswerDeadline','DeliveryManageDiv','is_Deleted',
    #        ),
    #extra=0,min_num=1,validate_min=True,can_delete=True
#)

    # 発注日
    #def clean_ProductOrderOrderingDate(self):
    #    ProductOrderOrderingDate = self.cleaned_data['ProductOrderOrderingDate']
    #    if ProductOrderOrderingDate:
    #        try:
    #            if not re.match(r'/^[0-9]{4}/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$/', ProductOrderOrderingDate):
    #                raise forms.ValidationError(u'yyyy-mm-dd形式で')
    #        except Exception:
    #            raise forms.ValidationError(u'日付に変換できません')
    #    return ProductOrderOrderingDate

