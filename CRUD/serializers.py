from rest_framework import serializers
from .models import MainTable


class MainTableSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    date_and_time_attention = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time_attention = serializers.TimeField(format="%H:%M")
    company = serializers.CharField(max_length = 100)
    city = serializers.CharField(max_length = 50)
    subject = serializers.CharField(max_length = 100)
    answer =  serializers.CharField()
    application_date = serializers.DateField(format="%Y-%m-%d")


    def create(self, validated_data):
        return MainTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.date_and_time_attention = validated_data.get('date_and_time_attention', instance.date_and_time_attention)
        instance.end_time_attention = validated_data.get('end_time_attention', instance.end_time_attention)
        instance.company = validated_data.get('company', instance.company)
        instance.city = validated_data.get('city', instance.city)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.answer = validated_data.get('answer', instance.answer)
        instance.application_date = validated_data.get('application_date', instance.application_date)
        instance.save()
        return instance