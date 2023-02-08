from rest_framework import serializers

from baseemail.models import EmailTemplate


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        exclude = ('id', )