from shared_models.models import Organization
from rest_framework import viewsets
from campuslibs.shared_utils.shared_function import PaginatorMixin, SharedMixin
from campuslibs.shared_utils.data_decorators import ViewDataMixin
from rest_framework.response import Response

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)

from app.serializers import GetOrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet, ViewDataMixin, PaginatorMixin):
    """
    A viewset for viewing employees.
    """
    serializer_class = GetOrganizationSerializer
    http_method_names = ["get", "head"]
    model = Organization

    def get_queryset(self):
        fields = self.request.GET.copy()
        try:
            fields.pop("limit")
            fields.pop("page")
        except KeyError:
            pass

        return self.model.objects.filter(**fields.dict())

    def retrieve(self, request, *args, **kwargs):
        org = self.get_object()
        serializer = self.serializer_class(org)
        return Response(self.object_decorator(serializer.data))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(self.paginate(serializer.data), status=HTTP_200_OK)
