from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.shortcuts import reverse


class Seller(models.Model):
    name = models.CharField(default='My Shop', max_length=30)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = ("Seller")
        verbose_name_plural = ("Sellers")
        ordering = ['name']
        db_table = 'seller'

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("Seller_detail", kwargs={"pk": self.pk})
