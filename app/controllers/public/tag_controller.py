from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.tags import tags_service

def index(request, slug):
  tag = tags_service.find_one(slug=slug)

  if not tag:
    return redirect('home')

  posts = posts_service.find_by_tag_id(tag.id.hex)

  return render(request, 'public/views/tag/tag.html', {
    'posts': posts,
    'tag': tag,
    'title': 'Từ khoá: ' + tag.name,
  })
