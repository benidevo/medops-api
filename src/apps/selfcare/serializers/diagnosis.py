from rest_framework import serializers


class IssueSerializer(serializers.Serializer):
    Name = serializers.CharField()
    Accuracy = serializers.IntegerField()


class SpecialisationSerializer(serializers.Serializer):
    Name = serializers.CharField()


class DiagnosisSerializer(serializers.Serializer):
    Issue = IssueSerializer()
    Specialisation = SpecialisationSerializer(many=True)


class GetDiagnosisSerializer(serializers.Serializer):
    yob = serializers.IntegerField(min_value=1900, max_value=2022)
    gender = serializers.ChoiceField(choices=["male", "female"])
    symptoms = serializers.ListField(child=serializers.IntegerField())
