from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.categories import categories_service

def index(request, slug, page = 1):
  category = categories_service.find_one(slug=slug)

  if category is None:
    return redirect('home')

  recent_posts_paginate = []
  limit = 21
  offset = (page - 1) * limit
  # Parent category
  if (category.parent_id is None):
    recent_posts_paginate = posts_service.find_recent_posts_by_parent_category(category_id=category.id, offset=offset, limit=limit)
  # Child category
  else:
    recent_posts_paginate = posts_service.find_recent_posts_paginate(offset=offset, limit=limit, category_id=category.id)

  recent_posts = posts_service.find_recent_posts()

  posts = recent_posts_paginate[0]
  total = recent_posts_paginate[1]

  return render(request, 'public/views/category/category.html', {
    'recent_posts': recent_posts,
    'recent_category_posts': posts,
    'page': page,
    'has_next': total - offset > limit,
    'category': category,
    'title': category.name,
  })
