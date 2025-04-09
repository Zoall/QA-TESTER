from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('<int:student_id>/update/', views.student_update,
         name='student_update'),  # Change pk to student_id
    path('<int:student_id>/delete/', views.student_delete,
         name='student_delete'),  # Change pk to student_id
]
