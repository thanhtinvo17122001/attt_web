import uuid
from django.db.models import UUIDField, TextField, ForeignKey, NOT_PROVIDED
from app.common.base_model import BaseModel

class Comments(BaseModel):
  id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  content = TextField()
  post = ForeignKey('Posts', null=True, on_delete=NOT_PROVIDED)
  user = ForeignKey('Users', null=True, on_delete=NOT_PROVIDED)

  class Meta:
    db_table = 'comments'