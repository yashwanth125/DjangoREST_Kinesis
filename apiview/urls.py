from django.urls import path

from . import views

urlpatterns = [
    path('demo', views.ContainerListView.as_view(), name='demo'),
    path('todos/completed', views.TodoCompletedList.as_view()),
    path('todos/', views.TodoListCreate.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    
    path('helper/', views.helper, name='helper'),
]