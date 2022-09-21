from rest_framework import serializers


class IssueSerializer(serializers.Serializer):
    ID = serializers.IntegerField()
    Name = serializers.CharField()
    Accuracy = serializers.IntegerField()
    Icd = serializers.CharField()
    IcdName = serializers.CharField()
    ProfName = serializers.CharField()
    Ranking = serializers.IntegerField()


class SpecialisationSerializer(serializers.Serializer):
    ID = serializers.IntegerField()
    Name = serializers.CharField()
    SpecialistID = serializers.IntegerField()


class DiagnosisSerializer(serializers.Serializer):
    Issue = IssueSerializer()
    Specialisation = SpecialisationSerializer(many=True)


class GetDiagnosisSerializer(serializers.Serializer):
    yob = serializers.IntegerField(min_value=1900, max_value=2022)
    gender = serializers.ChoiceField(choices=["male", "female"])
    symptoms = serializers.ListField(child=serializers.IntegerField())
