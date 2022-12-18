from app.modules.comments.comments_model import Comments
from app.modules.auth import auth_service
from django.utils import timezone

def find_many(**params):
  return Comments.objects.filter(**params).select_related('user', 'created_by').order_by('created_at')

def find_tree(**params):
  comments = list(Comments.objects.filter(**params).select_related('user', 'created_by').order_by('created_at'))
  parents = [c for c in comments if c.parent_id == None]
  for c in parents:
    c.children = [n for n in comments if n.parent_id == c.id]
  return parents

def create_comment(request, content, post_id, parent_id = None):
  auth = auth_service.get_auth_data(request)
  user_id = auth['auth_user_id']

  comment = Comments(
    content=content,
    post_id=post_id,
    user_id=user_id,
    parent_id=parent_id
  )

  comment.save()
  return comment

def update_comment(content, post_id, comment_id):
  comment = Comments.objects.filter(id=comment_id).first()

  if not comment: return
  comment.content = content
  comment.updated_at = timezone.now()
  comment.save()

  return comment

def delete(post_id, comment_id):
  Comments.objects.filter(id=comment_id, post_id = post_id).delete()
