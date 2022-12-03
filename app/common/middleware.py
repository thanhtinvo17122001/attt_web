from app.modules.auth import auth_service
from django.shortcuts import render, redirect

def app_middleware(get_response):
  def middleware(request):
    if (not request.path.startswith('/admin')):
      return get_response(request)
  
    auth = auth_service.get_auth_data(request)

    if (auth['auth_authenticated'] != True or auth['auth_role'] != 'ADMIN'):
      return redirect('home')

    return get_response(request)

  return middleware