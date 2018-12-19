from django.urls import include, path
from django.contrib.auth.models import User 
from rest_framework import routers, serializers, viewsets
from machinery.controllers import users, category, items, location, post, bids, transactions, advert
from machinery.help import helpers,adspricing


urlpatterns = [
    
    #User routes
    path('users/createuser/', users.create_user),
    path('users/updateuser/', users.update_user),
    path('users/user_device_uid/', users.user_device_uid),
    path('users/deleteuser/', users.delete_user),
    path('users/getallusers/', users.get_all_users),
    path('users/email_login/', users.get_user_email_login),
    path('users/resetuserpassword/',users.update_user_password),
    path('users/getparticularuser/', users.get_particular_user_details),
    path('users/user_device_uid/', users.user_device_uid),
    path('users/add_user_card/', users.add_user_card),

    #Transaction routes
    path('transactions/createstripecharge/', transactions.create_stripe_customer_charge),
    path('transactions/getcustomercards/', transactions.get_customer_cards),
    path('transactions/checkcustomerpaymentstatus/', transactions.check_user_payment_status),
    path('transactions/getstripebalance/', transactions.get_stripe_balance),
    path('transactions/stripepayout/', transactions.stripe_payout),
    path('transactions/getparticularusertransactions/', transactions.get_particular_user_transactions),

    #Category routes
    path('category/createcategory/', category.create_category),
    path('category/updatecategory/', category.update_category),
    path('category/deletecategory/', category.delete_category),
    path('category/getallcategories/', category.get_all_categories),
    path('category/getparticularcategory/', category.get_particular_category_details),

    #Item routes
    path('item/createitem/', items.create_item),
    path('item/updateitem/', items.update_item),
    path('item/deleteitem/', items.delete_item),
    path('item/getallitems/', items.get_all_items),
    path('item/getparticularitems/', items.get_particular_item),
    path('item/getparticularuseritems/', items.get_particular_user_items),
    path('item/upload_gallery_pics_items/', items.upload_multiple_pics_item),
    path('item/get_all_gallery_pics_items/', items.get_all_gallery_items),
    path('item/get_gallery_pics_for_item/', items.get_gallery_pics_for_item),

    #Location routes
    path('location/createlocation/', location.create_location),
    path('location/updatelocation/', location.update_location),
    path('location/deletelocation/', location.delete_location),
    path('location/getalllocations/', location.get_all_locations),
    path('location/getparticularlocation/', location.get_particular_location_details),


    #Posts routes
    path('post/createpost/', post.create_post),
    path('post/updatepost/', post.update_post),
    path('post/deletepost/', post.delete_post),
    path('post/getallposts/', post.get_all_posts),
    path('post/getparticularuserposts/', post.get_particular_user_posts),
    path('post/getspecificpost/', post.get_particular_post),
    path('post/searchpost/', post.search_for_posts),
    path('post/searchpost2/', post.search_for_posts_2),
    path('post/searchpost3/', post.search_for_posts_3),
    path('post/getallacceptedpostsforposter/', post.get_posts_for_accepted_bids),


    #Bids routes
    path('bids/createbid/', bids.create_bid),
    path('bids/updatebid/', bids.update_bid),
    path('bids/deletebids/', bids.delete_bid),
    path('bids/getallbids/', bids.get_all_bids),
    path('bids/getparticularuserbids/', bids.get_particular_user_bids),
    path('bids/getparticularpostbids/', bids.get_particular_posts_bids),
    path('bids/getspecificbid/', bids.get_particular_bid),
    path('bids/acceptbid/', bids.accept_bid),
    path('bids/getallacceptedbidsforposter/', bids.see_accepted_bids_poster),
    path('bids/getspecificacceptedbidforposter/', bids.see_specific_accepted_bid_poster),
    path('bids/getallacceptedbidsforbidder/', bids.see_accepted_bids_bidder),
    path('bids/getspecificacceptedbidforbidder/', bids.see_specific_accepted_bid_bidder),
    path('bids/getallacceptedbids/', bids.get_all_bids_accepted),

    #adverts pricing routes
    path('adpricing/createadpricing/', adspricing.create_pricing_adverts),
    path('adpricing/updateadpricing/', adspricing.update_advert_price),
    path('adpricing/deleteadpricing/', adspricing.delete_adspricing),
    path('adpricing/getalladpricing/', adspricing.get_all_adspricing),
    path('adpricing/getparticularadpricing/', adspricing.get_particular_adspricing_details),
    path('adpricing/showadvertsonapp/', adspricing.get_all_adverts_basing_pricing),
    path('adpricing/filteradvertsonapp/', adspricing.get_all_adverts_basing_location),

    path('adpricing/createadverts/', advert.create_advert),
    path('adpricing/updateadverts/', advert.update_advert),
    path('adpricing/deleteadverts/', advert.delete_advert),
    path('adpricing/getalladverts/', advert.get_all_adverts),
    path('adpricing/getparticularadverts/', advert.get_particular_advert_details),
    path('adpricing/getparticularuseradverts/', advert.get_particular_user_adverts),

]