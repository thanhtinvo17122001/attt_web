import uuid
from django.db.models import UUIDField, TextField, JSONField, ForeignKey, NOT_PROVIDED
from app.common.base_model import BaseModel

class Posts(BaseModel):
  id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  title = TextField()
  slug = TextField()
  thumbnail = TextField(null=True, default='https://aui.atlassian.com/aui/latest/docs/images/avatar-person.svg')
  description = TextField()
  content = TextField()
  tag_ids = JSONField(null=True)
  category = ForeignKey('Categories', null=True, on_delete=NOT_PROVIDED)

  class Meta:
    db_table = 'posts'