from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listings, name='listings'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('create/', views.create_listing, name='create'),
    path('api/create/', views.create_listing_api, name='create_api'),
    path('api/me/', views.get_my_listings, name='my_listings_api'),
    path('api/all/', views.get_all_listings, name='all_listings_api'),
    path('api/delete/<int:listing_id>/', views.delete_listing_api, name='delete_api'),
    path('api/toggle-status/<int:listing_id>/', views.toggle_listing_status_api, name='toggle_status_api'),
<<<<<<< HEAD
=======
    
    # 4. Page Routes: To serve the actual HTML files
    path('view/<int:pk>/', views.listing_detail, name='detail'),
>>>>>>> deb2760f18d5604cf91abcb458a7f3c989188b88
]
