from django.shortcuts import render, redirect
from app.modules.posts import posts_service
from app.modules.comments import comments_service
from app.modules.tags import tags_service

def index(request, category_slug, post_slug):
  post = posts_service.find_one(slug=post_slug)

  if post is None:
    return redirect('home')

  tags = tags_service.find_all(id__in=post.tag_ids)
  comments = comments_service.find_many(post_id=post.id)
  posts_service.increase_view_count(id=post.id)

  return render(request, 'public/views/post/post.html', {
    'post': post,
    'comments': comments,
    'tags': tags,
    'title': post.title,
  })
