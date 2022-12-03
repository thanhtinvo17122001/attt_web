
def login(request, user):
  request.session['auth_user_id'] = user.id.hex
  request.session['auth_authenticated'] = True
  request.session['auth_username'] = user.username
  request.session['auth_email'] = user.email
  request.session['auth_role'] = user.role
  request.user = user

def logout(request):
  del request.session['auth_user_id']
  del request.session['auth_authenticated']
  del request.session['auth_username']
  del request.session['auth_email']
  del request.session['auth_role']
  request.user = None

def get_auth_data(request):
  return {
    'auth_user_id': request.session.get('auth_user_id', None),
    'auth_authenticated': request.session.get('auth_authenticated', None),
    'auth_username': request.session.get('auth_username', False),
    'auth_email': request.session.get('auth_email', False),
    'auth_role': request.session.get('auth_role', False),
  }
