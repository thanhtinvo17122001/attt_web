from django.shortcuts import render
from app.modules.comments import comments_service
import json
from django.http import JsonResponse

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

def reply(request, post_id, comment_id):
  if (request.method == 'GET'): return

  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  comment = comments_service.create_comment(
    request,
    content=body['content'],
    post_id=post_id,
    parent_id=comment_id
  )

  return render(request, 'public/views/comments/comment_item.html', {
    'comment': comment,
    'isReply': True,
  })

def delete(request, post_id, comment_id):
  if (request.method == 'GET'): return

  comments_service.delete(post_id=post_id, comment_id=comment_id)

  return JsonResponse({ 'deleted': True })

def update(request, post_id, comment_id):
  if (request.method == 'GET'): return

  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  comments_service.update_comment(content=body['content'], post_id=post_id, comment_id=comment_id)

  return JsonResponse({ 'updated': True })
