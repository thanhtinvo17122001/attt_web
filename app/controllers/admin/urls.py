from django.urls import path
from . import categories_controller as categories
from . import users_controller as users
from . import tags_controller as tags
from . import posts_controller as posts

urlpatterns = [
  path('users', users.index, name='users_index'),
  path('users/add', users.add, name='users_add'),
  path('users/<uuid:id>', users.edit, name='users_edit'),
  path('users/delete/<uuid:id>', users.delete, name='users_delete'),

  path('categories', categories.index, name='categories_index'),
  path('categories/add', categories.add, name='categories_add'),
  path('categories/<uuid:id>', categories.edit, name='categories_edit'),
  path('categories/delete/<uuid:id>', categories.delete, name='categories_delete'),

  path('tags', tags.index, name='tags_index'),
  path('tags/add', tags.add, name='tags_add'),
  path('tags/<uuid:id>', tags.edit, name='tags_edit'),
  path('tags/delete/<uuid:id>', tags.delete, name='tags_delete'),

  path('posts', posts.index, name='posts_index'),
  path('posts/add', posts.add, name='posts_add'),
  path('posts/<uuid:id>', posts.edit, name='posts_edit'),
  path('posts/delete/<uuid:id>', posts.delete, name='posts_delete'),
]