from django.contrib import admin
from .models import Seller, Item, OldItem
# Register your models here.

admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(OldItem)
