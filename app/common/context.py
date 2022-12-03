from app.modules.categories import categories_service
from app.modules.posts import posts_service
from app.modules.auth import auth_service
from django.shortcuts import render, redirect

def public_pages_processor(request):
  if (request.path.startswith('/admin')):
    return {}

  top_view_posts = posts_service.find_top_view_posts_chunk(6, 2)
  categories = categories_service.find_tree()

  return {
    'categories': categories,
    'top_view_posts': top_view_posts,
  }

def app_processor(request):
  return auth_service.get_auth_data(request)
