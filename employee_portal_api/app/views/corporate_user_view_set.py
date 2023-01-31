from shared_models.models import CustomUser, Employee, CustomRole
from rest_framework import viewsets
from campuslibs.shared_utils.shared_function import PaginatorMixin, SharedMixin
from campuslibs.shared_utils.data_decorators import ViewDataMixin
from rest_framework.response import Response
from django_scopes import scopes_disabled

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from app.serializers import CustomUserSerializer


class CorporateUserViewSet(viewsets.ModelViewSet, ViewDataMixin, PaginatorMixin):
    """
    A viewset for viewing and editing Corporate(employee) User.
    """
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "post", "patch", "update"]
    model = CustomUser

    def get_queryset(self):
        fields = self.request.GET.copy()
        try:
            fields.pop("limit")
            fields.pop("page")
        except KeyError:
            pass

        return self.model.objects.filter(**fields.dict())

    def retrieve(self, request, *args, **kwargs):
        dept = self.get_object()
        serializer = self.serializer_class(dept)
        return Response(self.object_decorator(serializer.data))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(self.paginate(serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        try:
            employee = Employee.objects.get(pk=data.get('employee', None))
        except Employee.DoesNotExist:
            return Response(
                {
                    "error": {"message": "Employee does not exists"},
                    "status_code": 404,
                },
                status=HTTP_404_NOT_FOUND,
            )
        else:
            user_data = {
                'first_name': employee.profile.first_name,
                'last_name': employee.profile.last_name,
                'email': employee.profile.primary_email,
                'primary_contact_number': employee.profile.primary_contact_number if employee.profile.primary_contact_number else 'N\A', # required in user, optional in profile
                'username': data.get('username', None),
                'password': data.get('password', None),
                'custom_roles': ['677a08c1-3972-43ed-bdf4-2bccadab26c6']
            }
            serializer = CustomUserSerializer(data=user_data, context={"request": request})
            with scopes_disabled():
                serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.create_user(**user_data)

            user.db_context = request.user.db_context
            user.save()

            employee.user = user
            employee.save()

            serializer = CustomUserSerializer(user)

        return Response(self.object_decorator(serializer.data), status=HTTP_201_CREATED)
