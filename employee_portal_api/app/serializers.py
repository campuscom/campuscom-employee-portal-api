from rest_framework import serializers

from shared_models.models import (Store, StoreConfiguration, Product, Profile, ImportTask, CourseProvider, Permission,
                                  CustomRole, CourseEnrollment, Course, Section, CartItem, ProfileCommunicationMedium,
                                  ProfileLink, IdentityProvider, ProfilePreference, SeatBlockReservation,
                                  SeatReservation, StoreCompany, SeatReservationHistory, StoreDomain)

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
