from app.modules.users.users_model import Users, Status
from django.contrib.auth.hashers import make_password

def find_many():
  return Users.objects.select_related('created_by', 'updated_by').order_by('-updated_at')

def find_one(**params):
  return Users.objects.filter(**params).first()

def create(**payload):
  user = Users(
    username=payload['username'],
    password=make_password(payload['password']),
    role=payload['role'],
    status='ACTIVE'
  )
  user.save()

def update(user, **payload):
  if (payload['password'] != ''):
    user.password = payload['password']

  user.role = payload['role']
  user.status = payload['status']
  user.save()

def delete(id):
  Users.objects.get(id=id).delete()

