from campuslibs.shared_utils.shared_function import PaginatorMixin, SharedMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from django_scopes import scopes_disabled
from shared_models.models import Course, ProfileStore, StoreCourse, Profile, ProfileStoreBalanceSkill
from models.occupation.occupation_skill import OccupationSkill as OccupationSkillModel

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class SkillView(APIView, SharedMixin, PaginatorMixin):
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
        try:
            employee_profile = Profile.objects.get(primary_email=user.email)
        except Profile.DoesNotExist:
            return Response(
                {
                    "error": {"message": "User Profile doesn't exists"},
                    "status_code": 400,
                },
                status=HTTP_400_BAD_REQUEST,
            )

        data = []
        try:
            balance_skill = ProfileStoreBalanceSkill.objects.get(profile_store__profile=employee_profile)
        except ProfileStoreBalanceSkill.DoesNotExist:
            return Response(
                {
                    "error": {"message": "No data available for this user"},
                    "status_code": 400,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            for skill in balance_skill.skill:
                status = 'not_acquired' if balance_skill.skill[skill] == 'pending' else 'acquired'
                try:
                    skill_data = OccupationSkillModel.objects.get(id=skill)
                except Exception:
                    pass
                else:
                    data.append({
                        'status': status,
                        "name": str(skill_data.name),
                        "skill_type": str(skill_data.skill_type),
                        "hot": str(skill_data.hot)
                    })
        return Response(self.paginate(data), status=HTTP_200_OK)
