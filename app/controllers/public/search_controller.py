from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.categories import categories_service

def index(request, page = 1):
  q = request.GET.get('q', '').strip()
  search_posts = []

  if q == '':
    return render(request, 'public/views/search/search.html', {
      'search_posts': search_posts,
      'q': q,
    })

  limit = 10
  offset = (page - 1) * limit
  search_posts = posts_service.search_posts(offset=offset, limit=limit, title=q)
  posts = search_posts[0]
  total = search_posts[1]

  return render(request, 'public/views/search/search.html', {
    'search_posts': posts,
    'q': q,
    'title': 'Tìm kiếm: ' + q,
    'page': page,
    'has_next': total - offset > limit,
  })
