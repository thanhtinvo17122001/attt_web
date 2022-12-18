import uuid
from django.db.models import UUIDField, TextField, ForeignKey, NOT_PROVIDED, CASCADE
from app.common.base_model import BaseModel

class Comments(BaseModel):
  id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  content = TextField()
  post = ForeignKey('Posts', null=True, on_delete=NOT_PROVIDED)
  user = ForeignKey('Users', null=True, on_delete=NOT_PROVIDED)
  parent = ForeignKey('Comments', null=True, on_delete=CASCADE)

  class Meta:
    db_table = 'comments'