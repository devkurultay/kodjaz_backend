from django.contrib import admin

from .models import Exercise
from .models import Lesson
from .models import Submission
from .models import Subscription
from .models import Track
from .models import Unit


class TrackAdmin(admin.ModelAdmin):
    exclude = ('date_time_created', 'date_time_modified',)
    list_display = ('name', 'description', 'is_published')


class UnitAdmin(admin.ModelAdmin):
    exclude = ('date_time_created', 'date_time_modified',)
    list_display = ('name', 'description', 'is_published')


class TrackListFilter(admin.SimpleListFilter):
    title = 'track'
    parameter_name = 'track'

    def lookups(self, request, model_admin):
        list_of_tracks = []
        queryset = Track.objects.all()
        for track in queryset:
            list_of_tracks.append(
                (str(track.id), track.name)
            )
        return sorted(list_of_tracks, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(lesson__unit__track__id=self.value())
        return queryset


class LessonAdmin(admin.ModelAdmin):
    exclude = ('date_time_created', 'date_time_modified',)
    list_display = ('name', 'unit', 'get_track', 'badge', 'is_published')

    def get_track(self, obj):
        return obj.unit.track.name
    get_track.short_description = 'Track'
    get_track.admin_order_field = 'unit__track__name'


class ExerciseAdmin(admin.ModelAdmin):
    exclude = ('date_time_created', 'date_time_modified',)
    list_display = ('name', 'lesson', 'get_unit', 'get_track', 'karma', 'is_published')
    list_filter = (TrackListFilter,)

    def get_unit(self, obj):
        return obj.lesson.unit.name
    get_unit.short_description = 'Unit'
    get_unit.admin_order_field = 'lesson__unit__name'

    def get_track(self, obj):
        return obj.lesson.unit.track.name
    get_track.short_description = 'Track'
    get_track.admin_order_field = 'lesson__unit__track__name'


class SubmissionAdmin(admin.ModelAdmin):
    exclude = ('date_time_created', 'date_time_modified',)
    list_display = ('user', 'exercise', 'get_lesson', 'get_unit', 'get_track')

    def get_lesson(self, obj):
        return obj.exercise.lesson.name
    get_lesson.short_description = 'Lesson'
    get_lesson.admin_order_field = 'exercise__lesson__name'

    def get_unit(self, obj):
        return obj.exercise.lesson.unit.name
    get_unit.short_description = 'Unit'
    get_unit.admin_order_field = 'exercise__lesson__unit__name'

    def get_track(self, obj):
        return obj.exercise.lesson.unit.track.name
    get_track.short_description = 'Track'
    get_track.admin_order_field = 'exercise__lesson__unit__track__name'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('track', 'user', 'date_time_created')
    list_filter = (TrackListFilter,)


admin.site.register(Track, TrackAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
