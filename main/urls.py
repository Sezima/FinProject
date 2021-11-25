from django.urls import path

from main import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('departments/', views.DepartmentListView.as_view(), name='department'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-create'),
    path('department-update/<int:pk>/', views.DepartmentUpdateView.as_view()),
    path('department-delete/<int:pk>/', views.DepartmentDeleteView.as_view()),
]