from rest_framework import serializers

from shared_models.models import (Permission, CustomRole, Employee, Organization, OrganizationType, Department, Course,
                                  CustomUser, Profile, EmployeeAccount, CreditRequest, CreditRequestHistory,
                                  CourseProvider)

from django_scopes import scopes_disabled
from django.utils import timezone
from models.course.course import Course as CourseModel


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


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ('id', 'employee', 'amount', 'reason', 'status', 'approver_note', 'approved_by', 'approval_date')


class GetCreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ('id', 'ref_id', 'employee', 'amount', 'reason', 'status', 'approver_note', 'approved_by', 'approval_date')
        depth = 1


class CreditRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequestHistory
        fields = ('id', 'credit_request', 'employee', 'amount', 'reason', 'status', 'approver_note', 'approved_by', 'approval_date', 'activity_type')



class CourseProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProvider
        fields = ('id', 'name', 'code', 'course_provider_logo_uri', 'content_db_reference', 'refund_email',
                  'configuration')

        def validate_configuration(self, value):
            """
            Ensure configuration contains json data
            """

            if not isinstance(value, dict):
                raise serializers.ValidationError("value must be valid json")
            return value


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_provider', 'title', 'content_ready', 'slug', 'content_db_reference', 'course_image_uri',
                  'external_image_url', 'active_status')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course_provider'] = CourseProviderSerializer(
            CourseProvider.objects.get(id=data['course_provider'])).data

        if data['course_image_uri'] is None:
            data['course_image_uri'] = data['external_image_url']

        # skills details tagged with a course
        try:
            course_model = CourseModel.objects.get(pk=data['content_db_reference'])
        except CourseModel.DoesNotExist:
            data['skills'] = []
        else:
            data['skills'] = [
                {
                    "id": str(item.id),
                    "name": str(item.name),
                    "skill_type": str(item.skill_type),
                    "example": str(item.example),
                    "hot": str(item.hot),
                }
                for item in course_model.skills
            ]
        return data
