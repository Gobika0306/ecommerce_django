from django.contrib.auth.models import AbstractUser,Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
   
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)
    selected_permissions = models.ManyToManyField(Permission, blank=True)

    
    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    stock=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

from django.conf import settings
from django.db import models

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
