from django.shortcuts import render, redirect
from django.contrib import messages
from app.modules.categories import categories_service

def index(request):
  categories = categories_service.find_many()
  return render(request, 'admin/views/categories/index.html', { 'categories': categories })

def add(request):
  if request.method == 'GET':
    return add_get(request)

  return add_post(request)

def add_get(request):
  parents = categories_service.find_parents()
  return render(request, 'admin/views/categories/form.html', { 'parents': parents })

def add_post(request):
  payload = request.POST
  category = categories_service.find_one(name=payload['name'])

  if category is not None:
    parents = categories_service.find_parents()
    messages.error(request, 'Danh mục đã tồn tại')
    return render(request, 'admin/views/categories/form.html', { 'category': payload, 'parents': parents })

  categories_service.create(
    name=payload['name'],
    parent_id=payload['parent_id'] if payload['parent_id'] != '' else None
  )

  messages.success(request, 'Thêm danh mục thành công')
  return redirect('categories_index')

def edit(request, id):
  if request.method == 'GET':
    return edit_get(request, id)

  return edit_post(request, id)

def edit_get(request, id):
  category = categories_service.find_one(id=id)

  if category is None:
    return redirect('categories_index')

  parents = categories_service.find_parents()
  return render(request, 'admin/views/categories/form.html', { 'parents': parents, 'id': id, 'category': category })

def edit_post(request, id):
  payload = request.POST
  category = categories_service.find_one(id=id)

  if category is None:
    return redirect('categories_index')

  exist_category = categories_service.find_one_by_name_exclude_id(name=payload['name'], id=id)

  if exist_category is not None:
    parents = categories_service.find_parents()
    messages.error(request, 'Danh mục đã tồn tại')
    return render(request, 'admin/views/categories/form.html', { 'category': payload, 'parents': parents })

  categories_service.update(
    category=category,
    name = payload['name'],
    parent_id=payload['parent_id'] if payload['parent_id'] != '' else None
  )

  messages.success(request, 'Sửa danh mục thành công')
  return redirect('categories_index')

def delete(request, id):
  category = categories_service.find_one(id=id)

  if category is None:
    return redirect('categories_index')

  subs = categories_service.find_all(parent_id=id)
  if subs:
    messages.error(request, 'Không thể xoá danh mục cha')
    return redirect('categories_index')

  categories_service.delete(id)
  messages.success(request, 'Xoá danh mục thành công')
  return redirect('categories_index')