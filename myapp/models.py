from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20,null=True, blank=True)
    mob_no = models.CharField(max_length=12, null=True, blank=True, unique=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Others'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    image = models.ImageField(default='profiles/default.jpg', upload_to="profiles/", null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


class Categories(models.Model):
    category_name=models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="categories/",default="default.jpg", null=True, blank=True)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price =models.IntegerField()
    image=models.ImageField(upload_to='products', default=None)
    description = models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
      user = models.ForeignKey(User,on_delete=models.CASCADE)
      product = models.ForeignKey(Product,on_delete=models.CASCADE)
      quantity=models.IntegerField(default=1)

      def __str__(self):
          return self.product


class SellerProduct(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price =models.IntegerField()
    description = models.TextField()
    image=models.ImageField(upload_to='seller_products', default=None)
    accept=models.BooleanField(default=True)
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name   


class Payment(models.Model):
    amount=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    paytype=models.CharField(max_length=100)
    def __str__(self):
        return self.username


class Tracking(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    estimated_delivery = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Tracking {self.tracking_number} - {self.status}"
