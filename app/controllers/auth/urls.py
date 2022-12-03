from django.urls import path
from . import auth_controller as auth

urlpatterns = [
  path('dang-nhap', auth.login, name='login'),
  path('dang-xuat', auth.logout, name='logout'),
  path('trang-ca-nhan', auth.profile, name='profile'),
  path('doi-mat-khau', auth.update_password, name='update_password'),
  path('dang-ky', auth.register, name='register'),
  path('xac-nhan-dang-ky', auth.confirm_register, name='confirm_register'),
]
