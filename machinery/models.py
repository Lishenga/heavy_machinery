from django.db import models
import datetime

# Create your models here.
# user_status = 1 means active user

class users(models.Model):
    
    fname = models.CharField(max_length=255, default=None)
    lname = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=255, default=None, unique= True)
    password = models.CharField(max_length=255, default=None)
    status = models.IntegerField(default=0)
    role = models.CharField(max_length=255, default='POSTER')
    msisdn = models.CharField(max_length=255, default=None)
    device_uid = models.CharField(max_length=255, default='JESUS')
    stripe_id = models.CharField(max_length=255, default=None)
    card_brand = models.CharField(max_length=255, default=None)
    card_last_four = models.CharField(max_length=255, default=None)
    trial_end_at = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)


class category(models.Model):

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class user_items(models.Model):
    
    id = models.AutoField(primary_key=True)
    category_id = models.IntegerField(default=None)
    user_id = models.IntegerField(default=None)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    price_for_lease = models.CharField(max_length=500, default=None)
    location_id = models.IntegerField(default=None)
    pictures = models.CharField(max_length=500, default=None)
    pictures_thumb = models.CharField(max_length=500, default=None)
    min_radius = models.IntegerField(default=None)
    max_radius = models.IntegerField(default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

#user_items requested by user
class user_items_request(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=None)
    category_id = models.IntegerField(default=None)
    status = models.IntegerField(default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

#table for payments made by a user for a particular user_item
class user_items_payments(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=None)
    category_id = models.IntegerField(default=None)
    amount = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class logs(models.Model):
    
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, default=None)
    tags = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class feedback(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_item_id = models.IntegerField(default=None)
    description = models.CharField(max_length=255, default=None)
    rating = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class gallery_items(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=None)
    user_item_id = models.IntegerField(default=None)
    pictures = models.CharField(max_length=500, default=None)
    pictures_thumb = models.CharField(max_length=500, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class location(models.Model):
    
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=255, default=None)
    county = models.CharField(max_length=255, default=None)
    ward = models.CharField(max_length=255, default=None)
    province = models.CharField(max_length=255, default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class posts(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=None)
    location_id = models.IntegerField(default=None)
    category_id = models.IntegerField(default=1)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    min_days = models.CharField(max_length=500, default=None)
    max_days = models.CharField(max_length=500, default=None)
    price = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class bids(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.IntegerField(default=None)
    bidder_id = models.IntegerField(default=None)
    min_days = models.CharField(max_length=500, default=None)
    max_days = models.CharField(max_length=500, default=None)
    price = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

#accept bids
class bids_accept(models.Model):
    
    id = models.AutoField(primary_key=True)
    bid_id = models.IntegerField(default=None)
    post_id = models.IntegerField(default=None)
    bidder_id = models.IntegerField(default=None)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class transactions(models.Model):
    
    id = models.AutoField(primary_key=True)
    transaction_ref = models.CharField(max_length=500, default=None)
    user_id = models.IntegerField(default=None)
    amount = models.IntegerField(default=None)
    currency = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

#payment_status = 0 means not paid
class user_payment_status(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=None)
    payment_status = models.IntegerField(default=0)
    created_at = models.DateField(default=None)
    updated_at = models.DateField(default=None)

class adverts(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=None)
    location_id = models.IntegerField(default=None)
    category_id = models.IntegerField(default=1)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    pictures = models.CharField(max_length=500, default=None)
    price_id = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

class pricing_adverts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=500, default=None)
    days = models.CharField(max_length=500, default=None)
    time = models.CharField(max_length=500, default=None)
    price = models.CharField(max_length=500, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)

class adverts_logs(models.Model):
    id = models.AutoField(primary_key=True)
    advert_id = models.IntegerField(default=0)
    nexttime = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=None)
    updated_at = models.DateTimeField(default=None)