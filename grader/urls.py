from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('upload/', views.upload, name='upload'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:id>', views.course, name='course'),
    path('result/', views.check_result, name='check_result'),
]