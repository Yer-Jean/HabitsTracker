from datetime import timedelta

from rest_framework.exceptions import ValidationError


class HabitValidator:

    def __call__(self, value):
        try:
            if value['duration'] > timedelta(minutes=2):
                raise ValidationError('Duration of habit must be less or equal than 2 minutes')
        except KeyError:
            pass

        try:
            if not value['related_action'].is_pleasant:
                raise ValidationError('A related habit can only be a pleasant habit')
        except KeyError:
            pass

        try:
            if value['is_pleasant'] and (value.get('related_action') or value.get('reward')):
                raise ValidationError('An pleasant habit cannot have an related habit or reward')
        except KeyError:
            pass

        try:
            if value.get('related_action') and value.get('reward'):
                raise ValidationError('You can choose either a pleasant habit or a reward')
        except KeyError:
            pass
