from django.urls import path
from . import home_controller as home
from . import category_controller as category
from . import post_controller as post
from . import search_controller as search
from . import comment_controller as comments
from . import tag_controller as tags

urlpatterns = [
  path('comments/<uuid:post_id>', comments.comment, name='comment_post'),
  path('', home.index, name='home'),
  path('tim-kiem', search.index, name='search'),
  path('tu-khoa/<slug:slug>', tags.index, name='tag'),
  path('<slug:slug>', category.index, name='category'),
  path('<slug:category_slug>/<slug:post_slug>', post.index, name='post'),
]