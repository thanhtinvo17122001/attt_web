from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from app.modules.users import users_service

def index(request):
  users = users_service.find_many()
  return render(request, 'admin/views/users/index.html', { 'users': users })

def add(request):
  if request.method == 'GET':
    return add_get(request)

  return add_post(request)

def add_get(request):
  return render(request, 'admin/views/users/form.html')

def add_post(request):
  payload = request.POST
  user = users_service.find_one(username=payload['username'])

  if user is not None:
    messages.error(request, 'Người dùng đã tồn tại')
    return render(request, 'admin/views/users/form.html', { 'user': payload })

  users_service.create(
    username=payload['username'],
    password=make_password(payload['password']),
    role=payload['role'],
    status='ACTIVE'
  )

  messages.success(request, 'Thêm người dùng thành công')
  return redirect('users_index')

def edit(request, id):
  if request.method == 'GET':
    return edit_get(request, id)

  return edit_post(request, id)

def edit_get(request, id):
  user = users_service.find_one(id=id)

  if user is None:
    return redirect('users_index')

  user.password = ''
  return render(request, 'admin/views/users/form.html', { 'user': user, 'id': id })

def edit_post(request, id):
  payload = request.POST
  user = users_service.find_one(id=id)

  if user is None:
    return redirect('users_index')
  
  users_service.update(
    user=user,
    password=payload['password'],
    role=payload['role'],
    status=payload['status'],
  )

  messages.success(request, 'Sửa người dùng thành công')
  return redirect('users_index')

def delete(request, id):
  user = users_service.find_one(id=id)

  if user is None:
    return redirect('users_index')

  users_service.delete(id)
  messages.success(request, 'Xoá người dùng thành công')
  return redirect('users_index')