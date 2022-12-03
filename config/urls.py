from django.urls import include, path

urlpatterns = [
  path('admin/', include('app.controllers.admin.urls')),
  path('', include('app.controllers.auth.urls')),
  path('', include('app.controllers.public.urls')),
]