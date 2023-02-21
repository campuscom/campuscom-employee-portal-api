from campuslibs.shared_utils.shared_function import PaginatorMixin, SharedMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from django_scopes import scopes_disabled
from shared_models.models import Course, Profile, ProfileStoreBalanceSkill, ProfileStore, StoreCourse, Product
from models.course.course import Course as CourseModel

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.serializers import CourseSerializer

class CourseView(APIView, SharedMixin, PaginatorMixin):
    model = Course
    serializer_class = CourseSerializer
    http_method_names = ["get", "head"]

    def get_queryset(self):
        fields = self.request.GET.copy()
        try:
            fields.pop("limit")
            fields.pop("page")
        except KeyError:
            pass
        try:
            fields.pop("skills")
        except KeyError:
            pass

        return self.get_scoped_queryset(fields=fields)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        employee_skills = request.GET.get('skills', [])
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

        try:
            profile_balance = ProfileStoreBalanceSkill.objects.get(profile_store__profile=employee_profile)
            # if not employee_skills:
            #     employee_skills = [skill_id for skill_id in profile_balance.skill]
        except Exception:
            return Response(
                {
                    "error": {"message": "User don't have any store assigned"},
                    "status_code": 400,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            # filter with employee-user store
            queryset = queryset.filter(store_courses__store=profile_balance.profile_store.store)

        # filter with employee-user skill
        course_ids = []
        if employee_skills:
            for data in queryset:
                try:
                    course_model = CourseModel.objects.get(pk=data.content_db_reference)
                except CourseModel.DoesNotExist:
                    pass
                else:
                    for skill in course_model.skills:
                        if str(skill.id) in employee_skills:
                            course_ids.append(str(data.id))

            queryset = queryset.filter(id__in=course_ids)

        serializer = CourseSerializer(queryset, many=True)
        data = serializer.data

        # add products with courses
        for indx, course in enumerate(data):
            product_list = []
            try:
                with scopes_disabled():
                    store_course = StoreCourse.objects.get(store=profile_balance.profile_store.store, course=course['id'])
                    products = Product.objects.filter(store_course_section__store_course=store_course)
            except Exception:
                pass
            else:
                for product in products:
                    product_list.append({
                        'id': str(product.id),
                        'title': product.title
                    })
            data[indx]['products'] = product_list

        return Response(self.paginate(data), status=HTTP_200_OK)
