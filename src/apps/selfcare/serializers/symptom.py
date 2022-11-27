from rest_framework import serializers


class SymptomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
