from todos import views
from django.urls import path

urlpatterns = [
    path('', views.TodosAPIViews.as_view(), name='todos'),
    path('<int:id>', views.TodoDetailAPIView.as_view(), name='todo'),
]