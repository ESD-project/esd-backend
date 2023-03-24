from django.urls import path
from knox import views as knox_views
from . import views

app_name = "api"
urlpatterns = [
    path('', views.OverViewEndpoint.as_view(), name='overview'),
    path('register/', views.RegisterStaffAPI.as_view(), name="register"),
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
