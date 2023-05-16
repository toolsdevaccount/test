from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.forms import UserCreationForm
from .models import ProductOrder, FileUpload, CustomerSupplier

from django.forms import ModelChoiceField

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
    ManagerCode = ManagerChoiceField(queryset=get_user_model().objects.all(),empty_label='')
    ProductOrderApparelCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderDestinationCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderSupplierCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderShippingCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderCustomeCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')
    ProductOrderRequestCode = CustomerSupplierChoiceField(queryset=CustomerSupplier.objects.all(),empty_label='')

    class Meta:
        model = ProductOrder
        fields = ('ProductOrderMerchandiseCode', 'ProductOrderOrderingDate', 'ProductOrderSlipDiv', 'ProductOrderOrderNumber', 'ProductOrderPartNumber','ProductOrderApparelCode',
                  'ProductOrderDestinationCode','ProductOrderSupplierCode','ProductOrderShippingCode','ProductOrderCustomeCode','ProductOrderRequestCode','ProductOrderDeliveryDate',
                  'ProductOrderBrandName','ProductOrderUnitPrice','ProductOrderSellPrice','ProductOrderProcesefee')   

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

