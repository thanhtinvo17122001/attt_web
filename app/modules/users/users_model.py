import uuid
from django.db.models import UUIDField, TextField
from enum import Enum
from app.common.base_model import BaseModel

class Role(Enum):
  ADMIN = 'ADMIN'
  EDITOR = 'EDITOR'
  GUEST = 'GUEST'

class Status(Enum):
  ACTIVE = 'ACTIVE'
  DISABLED = 'DISABLED'
  PENDING = 'PENDING'

class Users(BaseModel):
  id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  username = TextField(255)
  password = TextField(255)
  email = TextField(max_length=255, null=True)
  full_name = TextField(max_length=255, null=True)
  author_name = TextField(max_length=255, null=True)
  avatar = TextField(max_length=255, null=True, default='https://aui.atlassian.com/aui/latest/docs/images/avatar-person.svg')
  role = TextField(255)
  status = TextField(255)
  otp = TextField(max_length=5, null=True)

  class Meta:
    db_table = 'users'