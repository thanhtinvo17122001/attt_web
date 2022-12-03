from app.modules.categories.categories_model import Categories
from django.utils.text import slugify 

def find_many():
  return Categories.objects.select_related('parent', 'created_by').order_by('-updated_at')

def find_all(**params):
  return Categories.objects.filter(**params)

def find_tree():
  categories = list(find_all())
  parents = [c for c in categories if c.parent_id == None]
  for c in parents:
    c.children = [n for n in categories if n.parent_id == c.id]
  return parents

def find_parents():
  return Categories.objects.filter(parent_id=None)

def find_subs():
  # return Categories.objects.filter(parent_id__isnull=False)
  return Categories.objects.filter()

def find_one(**params):
  return Categories.objects.filter(**params).first()

def find_one_by_name_exclude_id(name, id):
  return Categories.objects.filter(name=name).exclude(id=id).first()

def create(**payload):
  payload['slug'] = slugify(payload['name'])
  category = Categories(**payload)
  category.save()

def update(category, **payload):
  category.name = payload['name']
  category.slug = slugify(payload['name'])
  category.save()

def delete(id):
  Categories.objects.get(id=id).delete()

