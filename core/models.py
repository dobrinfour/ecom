from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.db.models import Avg
import math



class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category



class Item(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField( upload_to='background_pic',null=True,blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    
    description = models.TextField(null=True,blank=True)
    quantity = models.IntegerField(default=0)
    popular = models.BooleanField(default=False)
    new = models.BooleanField(default=False)


    def __str__(self):
        return self.title



    def get_sizes(self):

        if self.sizes != None:
            str = self.sizes
            list = str.split (",")

            return list
        else:
            return None

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})


    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'pk': self.pk})





class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.IntegerField(null=True,blank=True)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saveed(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    status = models.BooleanField(default=False)
    complete_date = models.DateTimeField(null=True)
    ref_code = models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.user.username


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


