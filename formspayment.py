from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.forms import UserCreationForm
from .models import Payment, DepoPayDiv

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

class PaymentDivChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.DepoPayDivname

class PaymentForm(forms.ModelForm):
    PaymentDiv = PaymentDivChoiceField(queryset=DepoPayDiv.objects.all(),empty_label='')

    class Meta:
        model = Payment
        fields = ('PaymentDate', 'PaymentSupplierCode', 'PaymentMoney', 'PaymentDiv', 'PaymentSummary' )

class PaymentSearchForm(forms.Form):
    query = forms.CharField(
        initial='',
        required = False, # 必須ではない
    )
