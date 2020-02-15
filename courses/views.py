import json

from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from django.views.generic.list import ListView

from . models import Track, Unit, Lesson, Exercise, Submission, SubmissionCreationException


class TracksListView(ListView):
    template_name = 'courses/tracks_list.html'
    model = Track

    def get_queryset(self):
        qs = super(TracksListView, self).get_queryset()
        return qs.filter(is_published=True)


class UnitsListView(ListView):
    model = Unit
    template_name = 'courses/units_list.html'

    def get_queryset(self):
        qs = super(UnitsListView, self).get_queryset()
        return qs.filter(track__id=self.kwargs['track_id'], is_published=True)


class LessonsListView(ListView):
    model = Lesson
    template_name = 'courses/lessons_list.html'

    def get_queryset(self):
        qs = super(LessonsListView, self).get_queryset()
        return qs.filter(unit__id=self.kwargs['unit_id'], is_published=True).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(LessonsListView, self).get_context_data(**kwargs)
        context['lessons_duration'] = self.get_queryset().aggregate(
            Sum('lesson_exercise__duration'))['lesson_exercise__duration__sum']
        return context


class ExerciseListView(ListView):
    model = Exercise
    template_name = 'courses/exercise_list.html'

    def get_queryset(self):
        qs = super(ExerciseListView, self).get_queryset()
        return qs.filter(lesson__id=self.kwargs['lesson_id'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super(ExerciseListView, self).get_context_data(**kwargs)
        context['lesson_duration'] = self.get_queryset().aggregate(Sum('duration'))['duration__sum']
        return context


class ExerciseTemplateView(TemplateView):
    template_name = 'courses/exercise.html'

    def get_context_data(self, **kwargs):
        context = super(ExerciseTemplateView, self).get_context_data(**kwargs)
        obj = Exercise.objects.get(id=kwargs['pk'])
        current_object = self._get_current_obj(obj)
        context['object'] = obj
        context['lecture'] = current_object.lecture
        context['instruction'] = current_object.instruction
        context['hint'] = current_object.hint
        context['default_code'] = self._get_default_code(current_object)
        context['unit_test'] = current_object.unit_test
        context['input_should_contain'] = current_object.input_should_contain
        context['input_should_not_contain'] = current_object.input_should_not_contain
        context['input_error_text'] = current_object.input_error_text
        context['output_should_contain'] = current_object.output_should_contain
        context['output_should_not_contain'] = current_object.output_should_not_contain
        context['output_error_text'] = current_object.output_error_text
        context['outputElementId'] = settings.OUTPUT_CONTAINER_ID_IN_EXERCISES_TEMPLATE
        return context

    def _get_current_obj(self, obj):
        try:
            return Submission.objects.get(exercise__id=obj.id, user=self.request.user)
        except Submission.DoesNotExist:
            return obj

    @staticmethod
    def _get_default_code(current_object):
        try:
            return current_object.default_code
        except AttributeError:
            return current_object.submitted_code


class CreateSubmissionView(CreateView):
    model = Submission

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'not_logged_in': True, 'saved': False})
        exercise = self._get_exercise(data)
        submitted_code = data['submitted_code']
        passed = json.loads(data['passed'])
        try:
            self.model.create_from_exercise(user=user, exercise=exercise, submitted_code=submitted_code, passed=passed)
            return JsonResponse({'saved': True})
        except SubmissionCreationException:
            return JsonResponse({'saved': False})

    @staticmethod
    def _get_exercise(data):
        exercise = Exercise.objects.get(pk=json.loads(data['exercise']))
        if exercise:
            return exercise
        return JsonResponse({'saved': False})
