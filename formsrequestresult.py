from django import forms
from django.contrib.auth import get_user_model
from .models import OrderingTable, OrderingDetail, RequestResult, DivSampleClass, DivOutputClass
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
        return  obj.CustomerCode + ":" + obj.CustomerOmitName[0:5]

class DivSampleClassChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.divname

class DivOutputClassChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.outputdivname

class RequestResultForm(forms.ModelForm):
    ManagerCode = ManagerChoiceField(queryset=get_user_model().objects.all(),empty_label='')
    SampleDiv = DivSampleClassChoiceField(queryset=DivSampleClass.objects.all(),empty_label='')
    OutputDiv = DivOutputClassChoiceField(queryset=DivOutputClass.objects.all(),empty_label='')
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['SampleDiv'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = OrderingTable
        fields = ('SlipDiv','OrderNumber','OrderingDate','StainShippingDate','ProductName','OrderingCount','StainPartNumber',
                  'StainMixRatio','DestinationCode','SupplierCode','ShippingCode','CustomeCode','StainShippingCode','RequestCode','SupplierPerson',
                  'TitleDiv','StockDiv','MarkName','OutputDiv','SampleDiv','is_Ordered','ManagerCode',
                 )

    # 手配先
    def clean_DestinationCode(self):
        DestinationCode = self.cleaned_data['DestinationCode']
        if DestinationCode == None:
            raise forms.ValidationError(u'このフィールドは必須です。')
        return DestinationCode
   
RequestResultFormset = forms.inlineformset_factory(
    OrderingTable, OrderingDetail, 
    fields=('DetailItemNumber','DetailColorNumber','DetailColor','DetailTailoring','DetailVolume','DetailUnitPrice',
            'DetailSellPrice','DetailPrice','DetailOverPrice','DetailSummary','SpecifyDeliveryDate','StainAnswerDeadline',
            'DeliveryManageDiv','PrintDiv','DetailUnitDiv',
            ),
    extra=0,min_num=1,validate_min=True,can_delete=True
)

RequestRecordFormset = forms.inlineformset_factory(
    OrderingTable, RequestResult, 
    fields=('ResultItemNumber','ResultDate','ShippingDate','ShippingVolume','SlipNumber','ResultSummary',
            'ResultMoveDiv','ResultGainDiv','ResultDecreaseDiv','OrderingDetailId'
            ),
    extra=0,min_num=1,validate_min=True,can_delete=True
)

#RequestRecordFormset = forms.inlineformset_factory(
#    OrderingTable, RequestResult,
#    fields=('ResultItemNumber','ResultDate','ShippingDate','ShippingVolume','SlipNumber','ResultSummary',
#            'ResultMoveDiv','ResultGainDiv','ResultDecreaseDiv','OrderingDetailId'
#            ),
#    extra=0,min_num=1,validate_min=True,can_delete=True
#)

class SearchForm(forms.Form):
    query = forms.CharField(
        initial='',
        required = False, # 必須ではない
    )
    key = forms.CharField(
        initial='',
        required=False,  # 必須ではない
    )
    word = forms.CharField(
        initial='',
        required=False,  # 必須ではない
    )
    orderdateFrom = forms.CharField(
        initial='',
        required=False,  # 必須ではない
    )
    orderdateTo = forms.CharField(
        initial='',
        required=False,  # 必須ではない
    )