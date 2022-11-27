import uuid
from django.db.models import UUIDField, TextField, BooleanField, SlugField
from app.common.base_model import BaseModel

class Tags(BaseModel):
  id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  name = TextField(max_length=255)
  slug = SlugField(max_length=255)
  is_hidden = BooleanField(default=False)

  class Meta:
    db_table = 'tags'