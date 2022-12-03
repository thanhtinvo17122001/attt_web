from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.categories import categories_service

def index(request, slug):
  category = categories_service.find_one(slug=slug)

  if category is None:
    return redirect('home')

  recent_category_posts = []
  # Parent category
  if (category.parent_id is None):
    recent_category_posts = posts_service.find_recent_posts_by_parent_category(category_id=category.id)
  # Child category
  else:
    recent_category_posts = posts_service.find_recent_posts(category_id=category.id)

  recent_posts = posts_service.find_recent_posts()

  return render(request, 'public/views/category/category.html', {
    'recent_posts': recent_posts,
    'recent_category_posts': recent_category_posts,
    'category': category,
  })
