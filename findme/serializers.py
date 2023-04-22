from rest_framework import serializers
from .models import Paragraph, Word

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['*']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['*']
