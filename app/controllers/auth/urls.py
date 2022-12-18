from django.urls import path
from . import auth_controller as auth

urlpatterns = [
  path('dang-nhap', auth.login, name='login'),
  path('dang-xuat', auth.logout, name='logout'),
  path('trang-ca-nhan', auth.profile, name='profile'),
  path('me/update-avatar', auth.update_avatar, name='update_avatar'),
  path('doi-mat-khau', auth.update_password, name='update_password'),
  path('doi-mat-khau-moi', auth.update_password_non_login, name='update_password_non_login'),
  path('quen-mat-khau', auth.forgot_password, name='forgot_password'),
  path('dang-ky', auth.register, name='register'),
  path('xac-nhan-dang-ky', auth.confirm_register, name='confirm_register'),
]
