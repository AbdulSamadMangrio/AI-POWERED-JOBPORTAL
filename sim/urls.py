from tkinter.font import names

from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobListingViewSet, JobSeekersViewSet, EmployerViewSet, RegistrationView, LoginView, \
    JobSeekersProfileView

router = DefaultRouter()
router.register(r'jobseekers', JobSeekersViewSet)
router.register(r'employers', EmployerViewSet)
router.register(r'joblisting', JobListingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('jobseekers/profile', JobSeekersProfileView.as_view(), name='jobseekers-profile')
]