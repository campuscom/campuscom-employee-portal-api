from rest_framework import serializers

from shared_models.models import (Permission, CustomRole, Employee, Organization, OrganizationType, Department)

from django_scopes import scopes_disabled
from django.utils import timezone


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'action', 'operation', 'group')


class CustomRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRole
        fields = ('id', 'name', 'permissions', 'menu_permissions')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'profile', 'user', 'organization', 'department', 'address', 'gender', 'is_active')


class GetEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'ref_id', 'profile', 'user', 'organization', 'department', 'address', 'gender', 'is_active')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'organization', 'name', 'short_name', 'description', 'is_active')

