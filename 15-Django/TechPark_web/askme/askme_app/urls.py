from django.contrib import admin
from django.urls import path
from askme_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('settings', views.settings, name='settings'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('sign_up/', views.signup, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot')
]
