from django.shortcuts import render
from app.modules.comments import comments_service
import json

def comment(request, post_id):
  if (request.method == 'GET'): return

  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  comment = comments_service.create_comment(
    request,
    content=body['content'],
    post_id=post_id,
  )

  return render(request, 'public/views/comments/comment_item.html', {
    'comment': comment,
  })
