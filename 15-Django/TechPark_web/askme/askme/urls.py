"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from askme_app import views
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.index, name='index'),
#     path('question/<int:question_id>/', views.question, name='question'),
#     path('settings', views.settings, name='settings'),
#     path('tag/<str:tag_name>/', views.tag, name='tag'),
#     path('sign_up/', views.signup, name='sign_up'),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('ask/', views.ask, name='ask'),
#     path('hot/', views.hot, name='hot')
# ]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from askme_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('askme_app.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # для запуска через gunicorn  askme.wsgi
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

