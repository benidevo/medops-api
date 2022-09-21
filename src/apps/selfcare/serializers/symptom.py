from rest_framework import serializers


class SymptomSerializer(serializers.Serializer):
    ID = serializers.IntegerField()
    Name = serializers.CharField()
