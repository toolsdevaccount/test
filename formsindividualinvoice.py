from django import forms
from django.contrib.auth import get_user_model
from .models import RequestResult ,OrderingTable
from betterforms.multiform import MultiModelForm # インポート

User = get_user_model()

class RequestResultForm(forms.ModelForm):
    class Meta:
        model = RequestResult
        fields = ('InvoiceNUmber',)

class OrderingTableForm(forms.ModelForm):
    class Meta:
        model = OrderingTable
        fields = ('OrderNumber', 'OrderingDate')

class IndividualMultiForm(MultiModelForm):
    form_classes = {
        "RequestResult_form": RequestResultForm, #（フォーム名：モデルフォームクラス名）
        "OrderingTable_form": OrderingTableForm,
    }

class IndividualSearchForm(forms.Form):
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
