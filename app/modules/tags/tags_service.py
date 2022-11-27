from app.modules.tags.tags_model import Tags
from django.utils.text import slugify 

def find_many():
  return Tags.objects.select_related('created_by', 'updated_by').order_by('-updated_at')

def find_one(**params):
  return Tags.objects.filter(**params).first()

def find_one_by_name_exclude_id(name, id):
  return Tags.objects.filter(name=name).exclude(id=id).first()

def create(**payload):
  tag = Tags(name=payload['name'], slug=slugify(payload['name']))
  tag.save()

def update(tag, **payload):
  tag.name = payload['name']
  tag.slug = slugify(payload['name'])
  tag.save()

def delete(id):
  Tags.objects.get(id=id).delete()
