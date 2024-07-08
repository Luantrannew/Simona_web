from django.db import models
from django.urls import reverse

class Product(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=50)
    unit_price = models.IntegerField()
    cat = models.ForeignKey("Category", on_delete=models.CASCADE,default=None)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.code})
    
    def __str__(self):
        return self.name

class Category(models.Model):
    cat_code = models.CharField(max_length=50,primary_key=True)
    cat_name = models.CharField(max_length=255)

    def __str__(self):
        return self.cat_code

class Customer(models.Model):
    code = models.CharField(max_length=9, primary_key=True) 
    name = models.CharField(max_length=100)
    seg = models.ForeignKey("CustomerSegments", on_delete=models.CASCADE,default=None)

    def get_absolute_url(self):
        return reverse("cus_detail", kwargs={"pk": self.code})
    
    def __str__(self):
        return self.name

class CustomerSegments(models.Model):
    seg_code = models.CharField(max_length=50, primary_key=True)
    seg_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.seg_code

class Order(models.Model):
    order_code = models.CharField(max_length=255, primary_key=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=False)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.order_code})
    
    def __str__(self):
        return self.order_code

class OrderLine(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField()
    
    def get_absolute_url(self):
        return reverse("order_line_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.pk}"
