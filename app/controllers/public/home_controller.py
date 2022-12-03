from django.shortcuts import render
from app.modules.posts import posts_service

def index(request):
  recent_posts = posts_service.find_recent_posts()
  top_view_posts = posts_service.find_top_view_posts(num_posts=12)
  slide_posts = list(top_view_posts)[:3]
  home_posts = list(top_view_posts)[3:]

  return render(request, 'public/views/home/home.html', {
    'recent_posts': recent_posts,
    'slide_posts': slide_posts,
    'home_posts': home_posts,
  })
