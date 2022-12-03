from django.db.models import Q
from app.modules.users.users_model import Users
from django.contrib.auth.hashers import make_password

def find_many():
  return Users.objects.select_related('created_by', 'updated_by').order_by('-updated_at')

def find_one(**params):
  return Users.objects.filter(**params).first()

def find_one_by_username_or_email(username_email):
  return Users.objects.filter(Q(email=username_email) | Q(username=username_email)).first()

def create(**payload):
  user = Users(
    email=payload['email'],
    username=payload['username'],
    password=make_password(payload['password']),
    role=payload['role'],
    status=payload['status'],
    otp=payload.get('otp', None)
  )
  user.save()

def update(user, **payload):
  if (payload['password'] != ''):
    user.password = payload['password']

  user.role = payload['role']
  user.status = payload['status']
  user.save()

def update_profile(user, **payload):
  user.full_name = payload['full_name']
  user.save()

def update_password(user, new_password):
  user.password = make_password(new_password)
  user.save()

def confirm_register(user):
  user.otp = None
  user.status = 'Active'
  user.save()

def delete(id):
  Users.objects.get(id=id).delete()

