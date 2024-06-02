from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Order, OrderLine, Product, Customer

class OrderForm(forms.ModelForm):
    time = forms.DateTimeField(initial=timezone.now())

    class Meta:
        model = Order
        fields = ['order_code', 'time', 'customer']

class OrderLineForm(forms.ModelForm):
    product_name = forms.ModelChoiceField(queryset=Product.objects.all(), label='Product name')

    class Meta:
        model = OrderLine
        fields = ['product_name', 'quantity']

OrderLineFormSet = inlineformset_factory  (Order, OrderLine, form=OrderLineForm, can_delete=True)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer    
        fields = ['code', 'name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'unit_price']
