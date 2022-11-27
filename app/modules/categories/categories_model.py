import uuid
from django.db.models import UUIDField, TextField, BooleanField, SlugField, ForeignKey, NOT_PROVIDED
from app.common.base_model import BaseModel

class Categories(BaseModel):
  id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  name = TextField()
  slug = SlugField()
  is_hidden = BooleanField(default=False)
  parent = ForeignKey('Categories', null=True, on_delete=NOT_PROVIDED)

  class Meta:
    db_table = 'categories'