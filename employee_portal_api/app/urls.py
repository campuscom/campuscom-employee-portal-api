"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView

from app.views import (health_check, MyTokenObtainPairView, EmployeeViewSet, DepartmentViewSet, OrganizationViewSet,
                       EmployeeAccountViewSet, CreditRequestViewSet, SkillView, CourseView)

router = routers.DefaultRouter()

router.register(r'employees', EmployeeViewSet, 'employees')
router.register(r'departments', DepartmentViewSet, 'departments')
router.register(r'organizations', OrganizationViewSet, 'organizations')
router.register(r'employee-accounts', EmployeeAccountViewSet, 'employee_accounts')
router.register(r'credit-requests', CreditRequestViewSet, 'credit_requests')


urlpatterns = [
    path('', include(router.urls)),
    path('check/', health_check),
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'skills/', SkillView.as_view(), name='skill'),
    path(r'courses/', CourseView.as_view(), name='courses'),
]
