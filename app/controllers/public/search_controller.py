from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.categories import categories_service

def index(request):
  q = request.GET.get('q', '').strip()
  search_posts = []

  if q == '':
    return render(request, 'public/views/search/search.html', {
      'search_posts': search_posts,
      'q': q,
    })

  search_posts = posts_service.search_posts(title=q)
  return render(request, 'public/views/search/search.html', {
    'search_posts': search_posts,
    'q': q,
    'title': 'Tìm kiếm: ' + q,
  })
