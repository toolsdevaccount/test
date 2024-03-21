from django import forms
from django.contrib.auth import get_user_model
from .models import RequestResult ,OrderingTable, CustomerSupplier
from betterforms.multiform import MultiModelForm # インポート
from django.forms import ModelChoiceField

User = get_user_model()

class CustomerSupplierChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.CustomerCode + ":" + obj.CustomerOmitName[0:5]

class RequestResultForm(forms.ModelForm):
    class Meta:
        model = RequestResult
        fields = ('InvoiceNUmber',)

class OrderingTableForm(forms.ModelForm):
    class Meta:
        model = OrderingTable
        fields = ('OrderNumber', 'OrderingDate')

class InvoiceMultiForm(MultiModelForm):
    form_classes = {
        "RequestResult_form": RequestResultForm, #（フォーム名：モデルフォームクラス名）
        "OrderingTable_form": OrderingTableForm,
    }

class InvoiceSearchForm(forms.Form):
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
    ShippingDateFrom = forms.CharField(
        initial='',
        required=False,  # 必須ではない
    )

class ClosingChoiceForm(forms.Form):
     invclosing = forms.fields.ChoiceField(
         choices = (
             (0, ""),
             (5, "5日"),
             (10, "10日"),
             (15, "15日"),
             (20, "20日"),
             (25, "25日"),
             (31, "末日"),
         ),
         required=True,
         widget=forms.widgets.Select
     )
