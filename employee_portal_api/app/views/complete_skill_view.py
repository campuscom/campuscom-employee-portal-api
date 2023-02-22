from campuslibs.shared_utils.data_decorators import ViewDataMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from shared_models.models import ProfileStoreBalanceSkill

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class CompleteSkillView(APIView, ViewDataMixin):
    http_method_names = ["post", "head"]

    def get_queryset(self):
        fields = self.request.GET.copy()
        try:
            fields.pop("limit")
            fields.pop("page")
        except KeyError:
            pass

        return self.get_scoped_queryset(fields=fields)

    def post(self, request, *args, **kwargs):
        user = request.user
        skills = request.data.get('skills', [])
        try:
            balance_skill = ProfileStoreBalanceSkill.objects.get(profile_store__profile__primary_email=user.email)
        except ProfileStoreBalanceSkill.DoesNotExist:
            return Response(
                {
                    "error": {"message": "There is no balance record for this User"},
                    "status_code": 400,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            for data in skills:
                for skill in balance_skill.skill:
                    if skill == data:
                        balance_skill.skill[skill] = 'complete'
                        continue
            balance_skill.save()

        return Response({'message': 'Successfully updated skill data'}, status=HTTP_200_OK)
