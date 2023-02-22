from campuslibs.shared_utils.data_decorators import ViewDataMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from shared_models.models import ProfileStoreBalanceSkill

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class ProfileDetailsView(APIView, ViewDataMixin):
    http_method_names = ["get", "head"]

    def get_queryset(self):
        fields = self.request.GET.copy()
        try:
            fields.pop("limit")
            fields.pop("page")
        except KeyError:
            pass

        return self.get_scoped_queryset(fields=fields)

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}
        try:
            profile_balance = ProfileStoreBalanceSkill.objects.get(profile_store__profile__primary_email=user.email)
        except ProfileStoreBalanceSkill.DoesNotExist:
            return Response(
                {
                    "error": {"message": "There is no balance record for this User"},
                    "status_code": 400,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            data['balance'] = profile_balance.balance

        return Response(self.object_decorator(data), status=HTTP_200_OK)
