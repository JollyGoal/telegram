from rest_framework import serializers

from .models import *


class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ('name',)


class TextSerializer(serializers.ModelSerializer):
    button = ButtonSerializer()

    class Meta:
        model = Text
        fields = ('button', 'text')
