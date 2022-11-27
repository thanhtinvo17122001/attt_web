from django.db.models import Model, DateTimeField, ForeignKey, NOT_PROVIDED

class BaseModel(Model):
  created_at = DateTimeField(auto_now_add=True)
  updated_at = DateTimeField(auto_now=True)
  created_by = ForeignKey('Users', related_name='%(class)s_created_by_name', db_column='created_by', null=True, on_delete=NOT_PROVIDED)
  updated_by = ForeignKey('Users', related_name='%(class)s_updated_by_name', db_column='updated_by', null=True, on_delete=NOT_PROVIDED)

  class Meta:
    abstract = True