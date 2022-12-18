from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from app.modules.users import users_service
from app.modules.auth import auth_service
from random_username.generate import generate_username
from app.common.helper import generateOtpCode
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from app.modules.cloudinary import cloudinary_service

def login(request):
  if request.method == 'GET':
    return login_get(request)

  return login_post(request)

def login_get(request):
  return render(request, 'public/views/auth/login.html')

def login_post(request):
  payload = request.POST
  user = users_service.find_one_by_username_or_email(username_email=payload['username_email'])

  if user.status != 'ACTIVE':
    messages.error(request, 'Tài khoản hiện không hoạt động')
    return redirect('login')

  if user is None or not check_password(payload['password'], user.password):
    messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu')
    return redirect('login')

  auth_service.login(request, user)
  return redirect('home')

def logout(request):
  auth_service.logout(request)
  return redirect('home')

def update_avatar(request):
  if request.method == 'GET':
    return

  auth = auth_service.get_auth_data(request)
  if not auth['auth_authenticated']:
    return JsonResponse({ 'url': None })

  user_id = auth['auth_user_id']
  user = users_service.find_one(id=user_id)

  if user is None:
    return JsonResponse({ 'url': None })

  file = request.FILES['file']
  url = cloudinary_service.upload_image(file)
  users_service.update_avatar(user=user, avatar=url)

  return JsonResponse({ 'url': url })

def profile(request):
  if request.method == 'GET':
    return profile_get(request)

  return profile_post(request)

def profile_get(request):
  auth = auth_service.get_auth_data(request)

  if not auth['auth_authenticated']:
    return redirect('home')
  
  user_id = auth['auth_user_id']
  user = users_service.find_one(id=user_id)

  if user is None:
    return redirect('home')
  
  return render(request, 'public/views/auth/profile.html', { 'user': user })

def profile_post(request):
  payload = request.POST
  auth = auth_service.get_auth_data(request)

  if not auth['auth_authenticated']:
    return redirect('home')

  user_id = auth['auth_user_id']
  user = users_service.find_one(id=user_id)

  if user is None:
    return redirect('home')

  users_service.update_profile(user=user, full_name=payload['full_name'])

  messages.success(request, 'Cập nhật thông tin thành công')
  return redirect('profile')

def update_password(request):
  if request.method == 'GET':
    return update_password_get(request)

  return update_password_post(request)

def update_password_get(request):
  auth = auth_service.get_auth_data(request)

  if not auth['auth_authenticated']:
    return redirect('home')

  user_id = auth['auth_user_id']
  user = users_service.find_one(id=user_id)

  if user is None:
    return redirect('home')

  return render(request, 'public/views/auth/update_password.html')

def update_password_post(request):
  payload = request.POST
  auth = auth_service.get_auth_data(request)

  if not auth['auth_authenticated']:
    return redirect('home')

  user_id = auth['auth_user_id']
  user = users_service.find_one(id=user_id)

  if user is None:
    return redirect('home')

  if not check_password(payload['password'], user.password):
    messages.error(request, 'Mật khẩu cũ không đúng')
    return redirect('update_password')

  if (payload['new_password'] != payload['confirm_password']):
    messages.error(request, 'Mật khẩu không trùng khớp')
    return redirect('update_password')

  users_service.update_password(user, new_password=payload['new_password'])
  messages.success(request, 'Cập nhật mật khẩu thành công')
  return redirect('update_password')


def register(request):
  if request.method == 'GET':
    return register_get(request)

  return register_post(request)

def register_get(request):
  return render(request, 'public/views/auth/register.html')

def register_post(request):
  payload = request.POST
  email = payload['email']
  user = users_service.find_one(email=email)

  if user is not None:
    messages.error(request, 'Email đã tồn tại')
    return redirect('register')

  otp = generateOtpCode()

  users_service.create(
    email=payload['email'],
    username=generate_username()[0],
    password=payload['password'],
    role='GUEST',
    status='PENDING',
    otp=otp
  )

  host = 'http://127.0.0.1:8000'
  link = f'{host}/xac-nhan-dang-ky?email={email}&code={otp}'
  mail_body = f'Vui lòng click vào link để hoàn tất đăng ký: <a href="{link}">{link}</a>'

  msg = EmailMultiAlternatives(
    subject='Đăng ký tài khoản web An toàn thông tin',
    body=mail_body,
    from_email='thanhtin1712.uit@gmail.com',
    to=[email],
  )
  msg.attach_alternative(mail_body, 'text/html')
  msg.send(fail_silently=False)

  messages.success(request, 'Vui kiểm tra email để hoàn tất đăng ký tài khoản')
  return redirect('register')

def confirm_register(request):
  email = request.GET.get('email', '').strip()
  otp = request.GET.get('code', '').strip()

  user = users_service.find_one(email=email)
  if user is None:
    messages.error(request, 'Xác nhận không thành công. Vui lòng liên hệ với admin.')
    return redirect('login')
  
  if user.otp != otp:
    messages.error(request, 'Xác nhận không thành công. Link không còn hiệu lực.')
    return redirect('login')

  users_service.confirm_register(user)

  messages.success(request, 'Xác nhận thành công. Bạn có thể đăng nhập ngay bây giờ.')
  return redirect('login')

def forgot_password(request):
  if request.method == 'GET':
    return forgot_password_get(request)

  return forgot_password_post(request)

def forgot_password_get(request):
  return render(request, 'public/views/auth/forgot_password.html')

def forgot_password_post(request):
  payload = request.POST
  email = payload['email']
  user = users_service.find_one(email=email)

  if user is None:
    messages.error(request, 'Email không tồn tại')
    return redirect('forgot_password')

  otp = generateOtpCode()

  users_service.update_otp(user, otp)

  host = 'http://127.0.0.1:8000'
  link = f'{host}/doi-mat-khau-moi?email={email}&code={otp}'
  mail_body = f'Vui lòng click vào link để thay đổi mật khẩu mới: <a href="{link}">{link}</a>'

  msg = EmailMultiAlternatives(
    subject='Đổi mật khẩu mới web An toàn thông tin',
    body=mail_body,
    from_email='thanhtin1712.uit@gmail.com',
    to=[email],
  )
  msg.attach_alternative(mail_body, 'text/html')
  msg.send(fail_silently=False)

  messages.success(request, 'Vui kiểm tra email để thay đổi mật khẩu mới')
  return redirect('forgot_password')

def update_password_non_login(request):
  if request.method == 'GET':
    return update_password_non_login_get(request)

  return update_password_non_login_post(request)

def update_password_non_login_get(request):
  email = request.GET.get('email', '').strip()
  otp = request.GET.get('code', '').strip()
  
  if (not email or not otp):
    messages.error(request, 'URL không hợp lệ.')
    return redirect('login')

  user = users_service.find_one(email=email)
  if user is None:
    messages.error(request, 'Xác nhận không thành công. Vui lòng liên hệ với admin.')
    return redirect('login')

  if user.otp != otp:
    messages.error(request, 'Xác nhận không thành công. Link không còn hiệu lực.')
    return redirect('login')

  return render(request, 'public/views/auth/update_password_non_login.html')

def update_password_non_login_post(request):
  payload = request.POST
  email = request.GET.get('email', '').strip()
  otp = request.GET.get('code', '').strip()

  if (not email or not otp):
    messages.error(request, 'URL không hợp lệ.')
    return redirect('login')

  user = users_service.find_one(email=email)
  if user is None:
    messages.error(request, 'Xác nhận không thành công. Vui lòng liên hệ với admin.')
    return redirect('login')

  if user.otp != otp:
    messages.error(request, 'Xác nhận không thành công. Link không còn hiệu lực.')
    return redirect('login')

  users_service.update_password(user, new_password=payload['new_password'])
  users_service.update_otp(user=user, otp=None)
  messages.success(request, 'Cập nhật mật khẩu thành công. Vui lòng đăng nhập với mật khẩu mới.')
  return redirect('login')