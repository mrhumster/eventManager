from django.contrib.auth.models import User
from rest_framework import serializers

from events import logger
from events.models import Task, Event, Guest


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(source='task_set', many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        """
        Добавляю в сериализованные данные задачи отметку о том
        что пользователь приславший запрос является исполнителем
        задачи. При инициализации сериализатора добавляется
        request в контекст.
        """
        ret = super().to_representation(instance)
        for task in ret['tasks']:
            request_guest_id = self.context.get('request', None).user.guest_set.filter(event=instance)[0].id
            if task['executor'] == request_guest_id:
                task['my'] = True
        return ret

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'

    person = PersonSerializer()

class VisitSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.CharField()
    email = serializers.EmailField()