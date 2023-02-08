from shared_models.models import CreditRequest, CreditRequestHistory
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

from app.serializers import CreditRequestSerializer, GetCreditRequestSerializer, CreditRequestHistorySerializer


class CreditRequestViewSet(viewsets.ModelViewSet, ViewDataMixin, PaginatorMixin):
    """
    A viewset for viewing and editing credit requests.
    """
    serializer_class = CreditRequestSerializer
    http_method_names = ["get", "head", "post", "patch", "update"]
    model = CreditRequest

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
        serializer = GetCreditRequestSerializer(employee)
        return Response(self.object_decorator(serializer.data))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GetCreditRequestSerializer(queryset, many=True)
        return Response(self.paginate(serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['status'] = 'pending'
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(self.object_decorator(serializer.data), status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            data.pop('id')
            data['activity_type'] = 'update'
            data['credit_request'] = instance
            data['employee'] = instance.employee
            data['approved_by'] = instance.approved_by
            CreditRequestHistory.objects.create(**data)
        return Response(self.object_decorator(serializer.data), status=HTTP_200_OK)
