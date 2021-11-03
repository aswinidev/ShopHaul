from django.db import models

# Create your models here.
class UserRegistration(models.Model):
    seller_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=20)
    Fname=models.CharField(max_length=20)
    Lname=models.CharField(max_length=20)
    address=models.CharField(max_length=200)
    contact_no=models.IntegerField(max_length=12)
    pswrd=models.CharField(max_length=20)
    class Meta:
        db_table = "Seller_info"