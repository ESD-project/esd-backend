from django.urls import path
from knox import views as knox_views
from . import views

app_name = "api"
urlpatterns = [
    path('', views.OverViewEndpoint.as_view(), name='overview'),
    path('register/', views.RegisterStaffAPI.as_view(), name="register"),
    path('register-user/', views.RegisterUserAPI.as_view(), name="register_user"),
]


# cars
urlpatterns += [
    path('cars/', views.CarListAPI.as_view(), name='car_list'),
    path('cars-detail/', views.CarDetailAPI.as_view(), name='car_detail'),
    path('create-update-car/', views.CreateUpdateCarAPI.as_view(), name='create_update_car'),  # noqa
    path('delete-car/', views.DeleteCarAPI.as_view(), name='car_update'),
]

# brand
urlpatterns += [
    path('brands/', views.BrandListAPI.as_view(), name='brands'),
    path('create-update-brand/', views.CreateUpdateBrandAPI.as_view(), name='create_update_brand'),  # noqa
    path('delete-brand/', views.DeleteBrandAPI.as_view(), name='delete-brand'),
]

# users
urlpatterns += [
    path('users/', views.UsersListAPI.as_view(), name='users'),
    path('users-brand/', views.DeleteUserAPI.as_view(), name='delete-user'),
]

# rentals
urlpatterns += [
    path('rentals/', views.RentalListAPI.as_view(), name='rental_list'),
    path('rentals-detail/', views.RentalDetailAPI.as_view(), name='rental_detail'),
    path('delete-rentals/', views.DeleteRentalAPI.as_view(), name='delete-rental'),
]

# rental slots
urlpatterns += [
    path('rental-slots/', views.RentalSlotListAPI.as_view(), name='rental_slot_list'),  # noqa
    path('rental-slots-detail/', views.RentalSlotDetailAPI.as_view(), name='rental_slot_detail'),  # noqa
    path('delete-rental-slot/', views.DeleteRentalSlotAPI.as_view(), name='delete_rental_slot'),  # noqa
]

# API AUTHENTICATION
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),  # noqa
]

# Profile urls
urlpatterns += [
    path('user-profile/', views.UserProfileAPI.as_view(), name='user_profile'),  # noqa
    path('change-password/', views.ChangePasswordAPI.as_view(), name='change_password'),  # noqa
]
