from django.urls import path, include
from rest_framework.routers import DefaultRouter
from userapp import views
from userapp.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('createUser/', views.createUser),
    # path('updateUser/<int:pk>/', views.updateUser),
    # path('patchUser/<int:pk>/', views.partialUpdateUser),
    # path('deleteUser/<int:pk>/', views.deleteUser),
    path('getUser/<int:user_id>/', views.getUserProfile),
    path('auth/login/', views.loginAccount),
]