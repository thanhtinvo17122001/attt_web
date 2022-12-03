from app.modules.comments.comments_model import Comments
from app.modules.auth import auth_service

def find_many(**params):
  return Comments.objects.filter(**params).select_related('user', 'created_by').order_by('updated_at')

def create_comment(request, content, post_id):
  auth = auth_service.get_auth_data(request)
  user_id = auth['auth_user_id']

  comment = Comments(
    content=content,
    post_id=post_id,
    user_id=user_id,
  )
  
  comment.save()
  return comment
