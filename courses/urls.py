from django.urls import path
from rest_framework import routers

from . import views
from courses.api_views import TrackViewSet
from courses.api_views import UnitViewSet
from courses.api_views import LessonViewSet
from courses.api_views import ExerciseViewSet

from courses.api_views import UserTrackViewSet
from courses.api_views import UserUnitViewSet
from courses.api_views import UserLessonViewSet
from courses.api_views import UserExerciseViewSet
from courses.api_views import UserSubmissionViewSet


app_name = 'courses'

router = routers.SimpleRouter()
router.register(r'api/v1/tracks', TrackViewSet)
router.register(r'api/v1/units', UnitViewSet)
router.register(r'api/v1/lessons', LessonViewSet)
router.register(r'api/v1/exercises', ExerciseViewSet)
router.register(r'api/v1/submissions', UserSubmissionViewSet, basename='Submission')

router.register(r'api/v1/user/tracks', UserTrackViewSet, basename='Track')
router.register(r'api/v1/user/units', UserUnitViewSet)
router.register(r'api/v1/user/lessons', UserLessonViewSet)
router.register(r'api/v1/user/exercises', UserExerciseViewSet)
router.register(r'api/v1/user/submissions', UserSubmissionViewSet, basename='Submission')

urlpatterns = [
    path('', views.TracksListView.as_view(), name='tracks_list'),
    path('track/<int:track_id>/', views.UnitsListView.as_view(), name='units_list'),
    path('unit/<int:unit_id>/', views.LessonsListView.as_view(), name='lessons_list'),
    path('lesson/<int:lesson_id>/', views.ExerciseListView.as_view(), name='exercises_list'),
    path('exercise/<int:pk>/', views.ExerciseTemplateView.as_view(), name='exercise'),
    path('create_submission', views.CreateSubmissionView.as_view(), name='create_submission'),
]

urlpatterns += router.urls
