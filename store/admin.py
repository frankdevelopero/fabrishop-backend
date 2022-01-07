from django.contrib import admin

# Register your models here.
from store.models import *

admin.site.register(CustomUser)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Gallery)
