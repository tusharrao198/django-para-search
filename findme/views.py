from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from findme.models import Paragraph, Word
from findme.serializers import ParagraphSerializer, WordSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paragraphs(request):
    paragraphs = request.data['paragraphs']
    paragraph_list = paragraphs.split('\n\n')
    for paragraph in paragraph_list:
        p = Paragraph.objects.create(text=paragraph)
        words = paragraph.split()
        for word in words:
            word = word.lower()
            w, created = Word.objects.get_or_create(text=word, paragraph=p)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_paragraphs(request, word):
    word = word.lower()
    word_paragraphs = Word.objects.filter(text=word).values_list('paragraph', flat=True).distinct()
    paragraphs = Paragraph.objects.filter(id__in=word_paragraphs)[:10]
    paragraph_texts = [p.text for p in paragraphs]
    return Response({'paragraphs': paragraph_texts})


# List all Api
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paragraph_list(request):
    # get all paragraphs
    paragraphs = Paragraph.objects.all()

    # serialize the paragraphs
    serializer = ParagraphSerializer(paragraphs, many=True)         

    return JsonResponse(serializer.data, safe=False)
