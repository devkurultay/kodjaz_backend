from django.urls import path

from . import views
from courses.api_views import TracksList


app_name = 'courses'

urlpatterns = [
    path('', views.TracksListView.as_view(), name='tracks_list'),
    path('track/<int:track_id>/', views.UnitsListView.as_view(), name='units_list'),
    path('unit/<int:unit_id>/', views.LessonsListView.as_view(), name='lessons_list'),
    path('lesson/<int:lesson_id>/', views.ExerciseListView.as_view(), name='exercises_list'),
    path('exercise/<int:pk>/', views.ExerciseTemplateView.as_view(), name='exercise'),
    path('create_submission', views.CreateSubmissionView.as_view(), name='create_submission'),

    path('api/v1/tracks/', TracksList.as_view(), name='api-tracks-list'),
]
