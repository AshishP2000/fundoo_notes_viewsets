"""fundoo_notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from note.views import Note, NoteCollaborator, Label, AddLabelToNote
from user.views import UserRegister, UserLogin, IsVerify

router = DefaultRouter()
router.register('user_register', UserRegister, basename='user_register')
router.register('user_login', UserLogin, basename='user_login')
# router.register('verify_user/<str:token>/', IsVerify, name='verify')
router.register('note', Note, basename='note')
router.register('collaborator', NoteCollaborator, basename='collaborator')
router.register('label', Label, basename='label')
router.register('label_note', AddLabelToNote, basename='label_note')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('verify_user/<str:token>/', IsVerify.as_view({'get':'list'}), name='verify')
]
