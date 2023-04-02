from rest_framework import serializers
from .models import Box

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'created_at', 'modified_at']

class BoxlistAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'created_at']


class BoxlistAllSerializerisStaff(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'created_by', 'created_at', 'modified_at']
