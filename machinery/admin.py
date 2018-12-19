from django.contrib import admin
from . models import user_items, category, users, user_items_request, gallery_items

admin.site.register(users)
admin.site.register(user_items_request)
admin.site.register(category)
admin.site.register(user_items)
admin.site.register(gallery_items)

# Register your models here.
