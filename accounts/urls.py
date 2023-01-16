
from django.urls import path

from . import views
from . views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLogin.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('',TaskList.as_view(),name='tasks'),
    # path('',views.list_venues,name='tasks'),
    path('task/<int:pk>/',TaskDetails.as_view(),name='details'),
    path('task_create',TaskCreate.as_view(),name='task_create'),
    path('task_update/<int:pk>/',TaskUpdate.as_view(),name='task_update'),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
]
