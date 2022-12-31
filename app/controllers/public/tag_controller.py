from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.tags import tags_service

def index(request, slug, page=1):
  tag = tags_service.find_one(slug=slug)

  if not tag:
    return redirect('home')

  limit = 10
  offset = (page - 1) * limit
  paginate = posts_service.find_by_tag_id(tag.id.hex, offset=offset, limit=limit)

  posts = paginate[0]
  total = paginate[1]

  return render(request, 'public/views/tag/tag.html', {
    'posts': posts,
    'tag': tag,
    'title': 'Từ khoá: ' + tag.name,
    'page': page,
    'has_next': total - offset > limit,
  })
