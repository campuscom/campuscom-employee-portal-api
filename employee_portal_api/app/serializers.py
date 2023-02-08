from rest_framework import serializers

from shared_models.models import (Permission, CustomRole, Employee, Organization, OrganizationType, Department,
                                  CustomUser, Profile, EmployeeAccount)

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

    def to_representation(self, instance):
            data = super().to_representation(instance)
            try:
                profile = Profile.objects.get(pk=data['profile'])
            except Profile.DoesNotExist:
                pass
            else:
                data['profile'] = {
                    'id': str(profile.id),
                    'name': profile.first_name + ' ' + profile.last_name,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'primary_email': profile.primary_email,
                }

            try:
                user = CustomUser.objects.get(pk=data['user'])
            except CustomUser.DoesNotExist:
                pass
            else:
                data['user'] = {
                    'id': str(user.id),
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username
                }

            try:
                organization = Organization.objects.get(pk=data['organization'])
            except Organization.DoesNotExist:
                pass
            else:
                data['organization'] = {
                    'id': str(organization.id),
                    'ref_id': str(organization.ref_id),
                    'name': organization.name,
                    'short_name': organization.short_name,
                    'description': organization.description,
                    'email': organization.email,
                    'contact_no': organization.contact_no,
                }

            try:
                department = Department.objects.get(pk=data['department'])
            except Department.DoesNotExist:
                pass
            else:
                data['department'] = {
                    'id': str(department.id),
                    'name': department.name,
                    'short_name': department.short_name
                }

            return data


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'organization', 'name', 'short_name', 'description', 'is_active')


class GetDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'organization', 'name', 'short_name', 'description', 'is_active')
        depth = 1


class GetOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'ref_id', 'name', 'short_name', 'organization_type', 'parent_organization', 'description', 'address', 'email', 'contact_no')
        depth = 1


class EmployeeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAccount
        fields = ('id', 'employee', 'order', 'credit_request', 'amount', 'transaction_type', 'note')


class GetEmployeeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAccount
        fields = ('id', 'ref_id', 'employee', 'order', 'credit_request', 'amount', 'transaction_type', 'note')
        depth = 1

