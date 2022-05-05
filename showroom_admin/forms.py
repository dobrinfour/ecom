from django import forms
from core.models import *

class ItemForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-control',}))
    
    class Meta():
        model = Item
        fields = ['title','image','price','discount_price','quantity','category','description','popular','new',]

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder': 'Item name',}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'discount_price':forms.NumberInput(attrs={'class':'form-control'}),
            # 'popular':forms.CheckboxInput(attrs={'class':'form-control'}),
            # 'new':forms.CheckboxInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'sizes':forms.TextInput(attrs={'class':'form-control'}),
        }



class ItemForm2(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-control',}))
    images = forms.ImageField(required = False,widget=forms.ClearableFileInput(attrs={'multiple': True,'class':'form-control'}))

    class Meta():
        model = Item
        fields = ['title','price','images','discount_price','quantity','category','description','popular','new',]

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder': 'Item name',}),
            # 'image':forms.FileInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'discount_price':forms.NumberInput(attrs={'class':'form-control'}),
            # 'popular':forms.CheckboxInput(attrs={'class':'form-control'}),
            # 'new':forms.CheckboxInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            
        }

    def save(self, commit=True):
        images = self.cleaned_data.pop('images')
        instance = super(ItemForm2, self).save()
        return instance

class CategoryForm(forms.ModelForm):

    class Meta():
        model = Category
        fields = ['category',]

        widgets = {
            'category':forms.TextInput(attrs={'class':'form-control','placeholder': 'new category',}),

        }


