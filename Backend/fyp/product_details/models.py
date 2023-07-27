from django.db import models

# Create your models here.
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=250)
    cat_image = models.ImageField (upload_to='cat_images')

class SubCategory(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=250)
    cat_id = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)

class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=250)
    p_image = models.ImageField(upload_to='product_images')
    p_brand = models.CharField(max_length=250)
    p_status = models.SmallIntegerField()
    p_des = models.TextField(max_length=5000)
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField()
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Variation(models.Model):
    v_id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
    quantity = models.IntegerField()
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)

class Wishlist(models.Model):
    w_id = models.AutoField(primary_key=True)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)

class CompareProducts(models.Model):
    c_id = models.AutoField(primary_key=True)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    user_data = models.ForeignKey("user_details.UserDetails", on_delete=models.CASCADE)

class MobilePhones(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    processor = models.CharField(max_length=500)
    battery = models.CharField(max_length=500)
    memory = models.CharField(max_length=500)
    display = models.CharField(max_length=500)
    camera = models.CharField(max_length=500)

class Laptops(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    processor = models.CharField(max_length=500)
    battery = models.CharField(max_length=500)
    memory = models.CharField(max_length=500)
    display = models.CharField(max_length=500)
    generation = models.IntegerField()

class LCD(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    display = models.CharField(max_length=500)
    power_consumption = models.CharField(max_length=500)
    audio = models.CharField(max_length=500)
    chip = models.CharField(max_length=500)

class AC(models.Model):
    category = models.ForeignKey("product_details.Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("product_details.SubCategory", on_delete=models.CASCADE)
    product = models.ForeignKey("product_details.Product", on_delete=models.CASCADE)
    capacity = models.CharField(max_length=500)
    type = models.CharField(max_length=500)
    inverter = models.BooleanField(default=True)
    warranty = models.IntegerField()
    energy_efficiency = models.IntegerField()


