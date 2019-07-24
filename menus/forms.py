from django import forms
from django.contrib.auth import get_user_model
from .models import Item
from restaurants.models import RestaurantLocation
User=get_user_model()
class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=[
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public'
        ]
    def __init__(self,user=None,*args,**kwargs):
        print(user)
        super(ItemForm,self).__init__(*args,**kwargs)
        self.fields['restaurant'].queryset=RestaurantLocation.objects.filter(owner=user)
