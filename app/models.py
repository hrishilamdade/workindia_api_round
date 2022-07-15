from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import secrets

PROFILE_CHOICES = (
    (1, 'Admin'),
    (2,'Customer')
)

class User(AbstractUser):
    
    user_type = models.IntegerField(choices = PROFILE_CHOICES)
    dob = models.DateField()
    aadhar_number = models.CharField(max_length=14)
    pancard_number = models.CharField(max_length=14)
    address = models.TextField()

    def __str__(self):
        return self.username


def get_account_no():
    return secrets.token_hex(16)

class Account(models.Model):

    account_no = models.CharField(primary_key=True, max_length=16,default=get_account_no)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="accounts")
    balance = models.DecimalField(decimal_places = 2,max_digits=10,default=0)
    account_state = models.CharField(max_length=10,default="active")
    last_transaction_timestamp = models.DateTimeField(blank=True,null=True)
