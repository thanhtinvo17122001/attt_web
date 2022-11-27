from django.shortcuts import render, redirect
from django.contrib import messages
from app.modules.tags.tags_model import Tags
from app.modules.tags import tags_service

def index(request):
  tags = tags_service.find_many()
  return render(request, 'admin/views/tags/index.html', { 'tags': tags })

def add(request):
  if request.method == 'GET':
    return add_get(request)

  return add_post(request)

def add_get(request):
  return render(request, 'admin/views/tags/form.html')

def add_post(request):
  payload = request.POST
  tag = tags_service.find_one(name=payload['name'])

  if tag is not None:
    messages.error(request, 'Thẻ đã tồn tại')
    return render(request, 'admin/views/tags/form.html', { 'tag': payload })

  tags_service.create(name=payload['name'])
  messages.success(request, 'Thêm thẻ thành công')

  return redirect('tags_index')

def edit(request, id):
  if request.method == 'GET':
    return edit_get(request, id)

  return edit_post(request, id)

def edit_get(request, id):
  tag = tags_service.find_one(id=id)

  if tag is None:
    return redirect('tags_index')

  return render(request, 'admin/views/tags/form.html', { 'id': id, 'tag': tag })

def edit_post(request, id):
  payload = request.POST
  tag = tags_service.find_one(id=id)

  if tag is None:
    return redirect('tags_index')

  exist_tag = tags_service.find_one_by_name_exclude_id(name=payload['name'], id=id)

  if exist_tag is not None:
    messages.error(request, 'Thẻ đã tồn tại')
    return render(request, 'admin/views/tags/form.html', { 'tag': payload })

  tags_service.update(tag=tag, name = payload['name'])

  messages.success(request, 'Sửa thẻ thành công')
  return redirect('tags_index')

def delete(request, id):
  tag = tags_service.find_one(id=id)

  if tag is None:
    return redirect('tags_index')

  tags_service.delete(id)
  messages.success(request, 'Xoá danh thẻ thành công')
  return redirect('tags_index')
