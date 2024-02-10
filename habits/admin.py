from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # list_display = ('owner', 'action', 'owner')
    list_filter = ('owner',)
