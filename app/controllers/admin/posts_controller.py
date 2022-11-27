from django.shortcuts import render, redirect
from django.contrib import messages
from app.modules.tags.tags_model import Tags
from app.modules.posts import posts_service
from app.modules.categories import categories_service

def index(request):
  posts = posts_service.find_many()
  return render(request, 'admin/views/posts/index.html', { 'posts': posts })

def add(request):
  if request.method == 'GET':
    return add_get(request)

  return add_post(request)

def add_get(request):
  subs = categories_service.find_subs()
  return render(request, 'admin/views/posts/form.html', { 'subs': subs })

def add_post(request):
  payload = request.POST
  post = posts_service.find_one(title=payload['title'])

  if post is not None:
    subs = categories_service.find_subs()
    messages.error(request, 'Bài viết đã tồn tại')
    return render(request, 'admin/views/posts/form.html', { 'post': payload, 'id': id, 'subs': subs })

  posts_service.create(
    title=payload['title'],
    description=payload['description'],
    category_id=payload['category_id'] if payload['category_id'] != '' else None,
    content=payload['content']
  )
  messages.success(request, 'Thêm bài viết thành công')

  return redirect('posts_index')

def edit(request, id):
  if request.method == 'GET':
    return edit_get(request, id)

  return edit_post(request, id)

def edit_get(request, id):
  post = posts_service.find_one(id=id)

  if post is None:
    return redirect('posts_index')

  subs = categories_service.find_subs()
  return render(request, 'admin/views/posts/form.html', { 'id': id, 'post': post, 'subs': subs })

def edit_post(request, id):
  payload = request.POST
  post = posts_service.find_one(id=id)

  if post is None:
    return redirect('posts_index')

  exist_post = posts_service.find_one_by_title_exclude_id(title=payload['title'], id=id)

  if exist_post is not None:
    subs = categories_service.find_subs()
    messages.error(request, 'Bài viết đã tồn tại')
    return render(request, 'admin/views/posts/form.html', { 'post': payload, id: 'id', 'subs': subs })

  posts_service.update(
    post=post,
    title = payload['title'],
    category_id=payload['category_id'] if payload['category_id'] != '' else None,
    description = payload['description'],
    content = payload['content'],
  )

  messages.success(request, 'Sửa bài viết thành công')
  return redirect('posts_index')

def delete(request, id):
  post = posts_service.find_one(id=id)

  if post is None:
    return redirect('posts_index')

  posts_service.delete(id)
  messages.success(request, 'Xoá bài viết thành công')
  return redirect('posts_index')