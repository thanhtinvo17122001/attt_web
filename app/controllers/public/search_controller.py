from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.categories import categories_service

def index(request):
  q = request.GET.get('q', '').strip()
  search_posts = []
  recent_posts = posts_service.find_recent_posts()

  if q == '':
    return render(request, 'public/views/search/search.html', {
      'recent_posts': recent_posts,
      'search_posts': search_posts,
      'q': q,
    })

  search_posts = posts_service.search_posts(title=q)
  return render(request, 'public/views/search/search.html', {
    'recent_posts': recent_posts,
    'search_posts': search_posts,
    'q': q
  })
