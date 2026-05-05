from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):

    ITEM_TYPE_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothes', 'Clothes'),
        ('documents', 'Documents'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)

    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE_CHOICES
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    created_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.item_type})"


class Claim(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, 
default='new')
    created_at = models.DateTimeField(auto_now_add=True)

class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='items/')

