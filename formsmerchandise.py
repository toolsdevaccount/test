from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.forms import UserCreationForm
from .models import Merchandise
from django.forms import ModelChoiceField

# バリデーション
import re

User = get_user_model()

class ManagerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return  obj.first_name + obj.last_name

class MerchandiseForm(forms.ModelForm):
    McdManagerCode = ManagerChoiceField(queryset=get_user_model().objects.all(),empty_label='')

    class Meta:
        model = Merchandise
        fields = ('McdCode', 'McdTreatmentCode', 'McdPartNumber','McdManagerCode',)
  
#OrderingFormset = forms.inlineformset_factory(
    #OrderingTable, OrderingDetail, 
    #fields=('DetailItemNumber','DetailColorNumber','DetailColor','DetailTailoring','DetailVolume','DetailUnitPrice',
    #        'DetailSellPrice','DetailPrice','DetailOverPrice','DetailSummary','SpecifyDeliveryDate','StainAnswerDeadline','DeliveryManageDiv','is_Deleted',
    #        ),
    #extra=0,min_num=1,validate_min=True,can_delete=True
#)
