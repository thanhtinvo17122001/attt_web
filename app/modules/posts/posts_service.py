from app.modules.posts.posts_model import Posts
from django.utils.text import slugify 

def find_many():
  return Posts.objects.select_related('created_by', 'category').order_by('-updated_at')

def find_one(**params):
  return Posts.objects.filter(**params).first()

def find_one_by_title_exclude_id(title, id):
  return Posts.objects.filter(title=title).exclude(id=id).first()

def create(**payload):
  payload['slug'] = slugify(payload['title'])
  post = Posts(**payload)
  post.save()

def update(post, **payload):
  post.title = payload['title']
  post.slug = slugify(payload['title'])
  post.category_id = payload['category_id']
  post.description = payload['description']
  post.content = payload['content']
  post.save()

def delete(id):
  Posts.objects.get(id=id).delete()

