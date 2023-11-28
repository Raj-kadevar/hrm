from django.urls import path

from .views import Login, PasswordReset, index, LoginAPI, IndexAPI, RegisterAPI, verification, leave, GetDevice, \
    AddLeaveAPI

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('index/', index, name="index"),
    path('registration/api/', RegisterAPI.as_view(), name="registration"),
    path('email-verification/<id>/', verification, name="email_verification"),

    path('leave/', leave, name="leave"),

    path('login/api/', LoginAPI.as_view(), name="login_api"),
    path('index/api/', IndexAPI.as_view(), name="index_api"),
    path('get-device/api/', GetDevice.as_view(), name="get_device"),
    path('add-leave/api/', AddLeaveAPI.as_view(), name="add_leave"),
    path('password-reset/', PasswordReset.as_view(), name="password_reset"),
]
