from django import forms
from django.contrib.auth import get_user_model
from .models import InvoiceNo

# バリデーション
import re

User = get_user_model()

class DailyUpdateForm(forms.ModelForm):

    class Meta:
        model = InvoiceNo
        fields = ('InvoiceNo', 'SInvoiceNo')