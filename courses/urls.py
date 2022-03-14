from django.urls import path,include
from . import views

app_name="courses"

urlpatterns = [
    path('<str:pk>/module/',views.CourseModuleUpdateView.as_view(),name='course_module_update'),
    path('mine/',views.ManageCourseListView.as_view(),name='manage_course_list'),
    path('create/',views.CourseCreateView.as_view(),name='course_create'),
    path('<int:pk>/edit/',views.CourseUpdateView.as_view(),name='course_edit'),
    path('<int:pk>/delete/',views.CourseDeleteView.as_view(),name='course_delete'),
]