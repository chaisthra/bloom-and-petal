from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'stock', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['available'].widget.attrs['class'] = 'form-check-input'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductImportForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with product data. The file should have the following columns: name, description, price, category, stock, available'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csv_file'].widget.attrs.update({
            'class': 'form-control',
            'accept': '.csv'
        })