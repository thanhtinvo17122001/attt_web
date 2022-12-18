from django.shortcuts import render
from app.modules.posts import posts_service

def index(request):
  recent_posts = posts_service.find_recent_posts()
  top_view_posts = posts_service.find_top_view_posts(num_posts=12)
  slide_posts = list(top_view_posts)[:3]
  home_posts = list(top_view_posts)[3:]
  attt_posts = posts_service.find_recent_posts(num=9, category__slug='an-toan-thong-tin')
  cntt_posts = posts_service.find_recent_posts(num=9, category__slug='cong-nghe-thong-tin')
  anqp_posts = posts_service.find_recent_posts(num=9, category__slug='an-ninh-quoc-phong')
  ctxh_posts = posts_service.find_recent_posts(num=9, category__slug='chinh-tri---xa-hoi')

  return render(request, 'public/views/home/home.html', {
    'recent_posts': recent_posts,
    'slide_posts': slide_posts,
    'home_posts': home_posts,
    'attt_posts': attt_posts,
    'cntt_posts': cntt_posts,
    'anqp_posts': anqp_posts,
    'ctxh_posts': ctxh_posts,
  })
