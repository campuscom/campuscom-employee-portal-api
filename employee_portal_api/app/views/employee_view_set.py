from shared_models.models import Employee, CustomUser, Profile
from rest_framework import viewsets
from campuslibs.shared_utils.shared_function import PaginatorMixin, SharedMixin
from campuslibs.shared_utils.data_decorators import ViewDataMixin
from rest_framework.response import Response

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)

from app.serializers import EmployeeSerializer, GetEmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet, ViewDataMixin, PaginatorMixin):
    """
    A viewset for viewing and editing employees.
    """
    serializer_class = EmployeeSerializer
    http_method_names = ["get", "head", "post", "patch", "update"]
    model = Employee

    def get_queryset(self):
        fields = self.request.GET.copy()
        try:
            fields.pop("limit")
            fields.pop("page")
        except KeyError:
            pass

        return self.model.objects.filter(**fields.dict())

    def retrieve(self, request, *args, **kwargs):
        employee = self.get_object()
        serializer = GetEmployeeSerializer(employee)
        return Response(self.object_decorator(serializer.data))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GetEmployeeSerializer(queryset, many=True)
        return Response(self.paginate(serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user = data.get('user', None)
        try:
            user_data = CustomUser.objects.get(pk=user)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    "error": {"message": "user does not exist"},
                    "status_code": 400,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                profile = Profile.objects.get(primary_email=user_data.email)
            except Profile.DoesNotExist:
                return Response(
                    {
                        "error": {"message": "profile does not exist for this user"},
                        "status_code": 400,
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
            else:
                data['profile'] = str(profile.id)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(self.object_decorator(serializer.data), status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        user = data.get('user', None)
        if user:
            try:
                user_data = CustomUser.objects.get(pk=user)
            except CustomUser.DoesNotExist:
                return Response(
                    {
                        "error": {"message": "user does not exist"},
                        "status_code": 400,
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
            else:
                try:
                    profile = Profile.objects.get(primary_email=user_data.email)
                except Profile.DoesNotExist:
                    return Response(
                        {
                            "error": {"message": "profile does not exist for this user"},
                            "status_code": 400,
                        },
                        status=HTTP_400_BAD_REQUEST,
                    )
                else:
                    data['profile'] = str(profile.id)
        serializer = self.serializer_class(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(self.object_decorator(serializer.data), status=HTTP_200_OK)
