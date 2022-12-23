import jwt
import json

from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, TemplateView
from django.views.generic.list import ListView

from . models import Track, Unit, Lesson, Exercise, Submission, SubmissionCreationException

User = get_user_model()


class LoginJWTUserMixin:
    """
    This mixin is used to create or log in a user
    which was passed via a JWT token.
    JWT should be created a secret key which is created using
    our secret key (see settings.JWT_SECRET)
    In this particular case we are creating/logging in a Laravel user.
    """
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            user_data = jwt.decode(token,
                                   settings.JWT_SECRET,
                                   'HS256')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            email = user_data.get('email')
            username = user_data.get('username')
            name = '{} {}'.format(first_name, last_name)
            password = 'bcrypt$' + user_data.get('password')
            if email is not None and password is not None:
                user, _ = User.objects.get_or_create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    name=name, email=email,
                    password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            else:
                # TODO(murat): Send info to the JWT sender that the token
                # didn't have all the required data
                pass
        return super().get(self, request, *args, **kwargs)


class TracksListView(LoginJWTUserMixin, ListView):
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
        return qs.filter(track__id=self.kwargs['track_id'], is_published=True).order_by('id')


class LessonsListView(ListView):
    model = Lesson
    template_name = 'courses/lessons_list.html'

    def get_queryset(self):
        qs = super(LessonsListView, self).get_queryset()
        return qs.filter(unit__id=self.kwargs['unit_id'], is_published=True).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(LessonsListView, self).get_context_data(**kwargs)
        context['lessons_duration'] = self.get_queryset().aggregate(
            Sum('lesson_exercises__duration'))['lesson_exercises__duration__sum']
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
        new_context = {
            'object': obj,
            'lecture': current_object.exercise.lecture,
            'instruction': current_object.exercise.instruction,
            'hint': current_object.exercise.hint,
            'default_code': self._get_default_code(current_object),
            'unit_test': current_object.exercise.unit_test,
            'input_should_contain': current_object.exercise.input_should_contain,
            'input_should_not_contain': current_object.exercise.input_should_not_contain,
            'input_error_text': current_object.exercise.input_error_text,
            'output_should_contain': current_object.exercise.output_should_contain,
            'output_should_not_contain': current_object.exercise.output_should_not_contain,
            'output_error_text': current_object.exercise.output_error_text,
            'outputElementId': settings.OUTPUT_CONTAINER_ID_IN_EXERCISES_TEMPLATE,
            'text_file_content': current_object.exercise.text_file_content,
            'programming_language': obj.lesson.unit.track.programming_language
        }
        context.update(new_context)
        return context

    def _get_current_obj(self, obj):
        if not self.request.user.is_authenticated:
            return obj
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
        text_file_content = data['text_file_content']
        passed = json.loads(data['passed'])
        try:
            self.model.create_from_exercise(
                user=user,
                exercise=exercise,
                submitted_code=submitted_code,
                text_file_content=text_file_content,
                passed=passed)
            return JsonResponse({'saved': True})
        except SubmissionCreationException:
            return JsonResponse({'saved': False})

    @staticmethod
    def _get_exercise(data):
        exercise = Exercise.objects.get(pk=json.loads(data['exercise']))
        if exercise:
            return exercise
        return JsonResponse({'saved': False})
