from django.db.models import Q, F
from app.modules.posts.posts_model import Posts
from app.modules.categories.categories_model import Categories
from django.utils.text import slugify 
from app.common.helper import chunks 

def find_many():
  return Posts.objects.select_related('created_by', 'category').order_by('-updated_at')

def find_by_tag_id(tag_id, offset=0, limit=10):
  query = Posts.objects.filter(tag_ids__contains=tag_id).select_related('category').order_by('-updated_at')
  return [query[offset:offset + limit], query.count()]

def search_posts(title, offset = 0, limit = 10):
  query = Posts.objects.filter(title__icontains=title).select_related('category').order_by('-view_count', '-updated_at')
  return [query[offset:offset + limit], query.count()]

def find_recent_posts(num=20,**params):
  return Posts.objects.filter(**params).select_related('category').order_by('-updated_at')[:num]

def find_recent_posts_paginate(offset = 0, limit = 50, **params):
  query = Posts.objects.filter(**params).select_related('category').order_by('-updated_at')
  return [query[offset:offset + limit], query.count()]

def find_recent_posts_by_parent_category(category_id, offset = 10, limit = 50):
  category_ids = Categories.objects.filter(Q(parent_id=category_id) | Q(id=category_id)).values_list('id')
  query =  Posts.objects.filter(category_id__in=category_ids).select_related('category').order_by('-updated_at')

  return [query[offset:offset + limit], query.count()]

def find_top_view_posts(num_posts):
  return Posts.objects.select_related('category').order_by('-view_count', '-updated_at')[:num_posts]

def find_top_view_posts_chunk(num_posts, chunk_length):
  posts = find_top_view_posts(num_posts)
  return chunks(list=list(posts), n=chunk_length)

def find_one(**params):
  return Posts.objects.select_related('category').filter(**params).first()

def increase_view_count(id):
  return Posts.objects.filter(id=id).update(view_count=F('view_count') + 1)

def find_one_by_title_exclude_id(title, id):
  return Posts.objects.filter(title=title).exclude(id=id).first()

def create(**payload):
  payload['slug'] = slugify(payload['title'])
  post = Posts(**payload)
  post.save()

def insert(**payload):
  post = Posts(**payload)
  post.save()
  return post

def update(post, **payload):
  post.title = payload['title']
  post.slug = slugify(payload['title'])
  post.category_id = payload['category_id']
  post.description = payload['description']
  post.content = payload['content']
  post.save()

def delete(id):
  Posts.objects.get(id=id).delete()

