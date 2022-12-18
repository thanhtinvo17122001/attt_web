from app.modules.users import users_service

def login(request, user):
  request.session['auth_user_id'] = user.id.hex
  request.session['auth_authenticated'] = True
  request.session['auth_username'] = user.username
  request.session['auth_email'] = user.email
  request.session['auth_role'] = user.role
  request.session['auth_avatar'] = user.avatar
  request.session['auth_full_name'] = user.full_name
  request.user = user

def logout(request):
  del request.session['auth_user_id']
  del request.session['auth_authenticated']
  del request.session['auth_username']
  del request.session['auth_email']
  del request.session['auth_role']
  del request.session['auth_avatar']
  del request.session['auth_full_name']
  request.user = None

def get_auth_data(request):
  user_id = request.session.get('auth_user_id', None)

  if not user_id:
    return {}

  user = users_service.find_one(id=user_id)

  return {
    'auth_user_id': user.id.hex,
    'auth_authenticated': True,
    'auth_username': user.username,
    'auth_email': user.email,
    'auth_role': user.role,
    'auth_avatar': user.avatar,
    'auth_full_name': user.full_name,
  }
