from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from django.shortcuts import render
from .models import Box
from .serializers import BoxSerializer


A1 = 100
V1 = 1000
L1 = 100
L2 = 50

# Add API
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_box(request):
    data = request.data
    user = request.user

    print(data, "\n", user)
    
    # Check if user has exceeded the limit of boxes added in a week
    week_ago = timezone.now() - timedelta(days=7)
    boxes_added_this_week = Box.objects.filter(created_by=user, created_at__gte=week_ago).count()
    if boxes_added_this_week >= L2:
        return Response({'error': 'User has exceeded the limit of boxes added in a week.'}, status=400)
    
    serializer = BoxSerializer(data=data)
    if serializer.is_valid():
        # Check if average area and volume of all boxes do not exceed their limits
        all_boxes = Box.objects.all()
        all_boxes_area = sum([box.length * box.breadth for box in all_boxes])
        all_boxes_volume = sum([box.length * box.breadth * box.height for box in all_boxes])
        new_box_area = data['length'] * data['breadth']
        new_box_volume = data['length'] * data['breadth'] * data['height']
        if (all_boxes_area + new_box_area) / all_boxes.count() > A1:
            return Response({'error': 'Average area of all boxes exceed limit.'}, status=400)
        if (all_boxes_volume + new_box_volume) / all_boxes.count() > V1:
            return Response({'error': 'Average volume of all boxes exceed limit.'}, status=400)
        
        # Create and save the new box
        serializer.save(created_by=user)
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)


# Update API
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_box(request, pk):
    box = get_object_or_404(Box, pk=pk)
    
    # Check if the user is trying to update the creator or creation date
    if request.user != box.created_by:
        return JsonResponse({'error': 'You are not allowed to update the creator or creation date.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BoxSerializer(box, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Check the average area condition
        boxes = Box.objects.all()
        total_area = sum(box.get_area() for box in boxes)
        average_area = total_area / len(boxes)
        a1 = 100 # Default value, should be configured externally
        if average_area + serializer.validated_data['area'] / len(boxes) > a1:
            return JsonResponse({'error': f'The average area of all boxes should not exceed {a1}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check the average volume condition
        user_boxes = Box.objects.filter(created_by=request.user)
        total_volume = sum(box.get_volume() for box in user_boxes)
        v1 = 1000 # Default value, should be configured externally
        if total_volume + serializer.validated_data['volume'] > v1:
            return JsonResponse({'error': f'Your average volume of all boxes should not exceed {v1}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check the total boxes added in a week condition
        week_boxes = Box.objects.filter(created_at__week=request.data['created_at'].isocalendar()[1])
        l1 = 100 # Default value, should be configured externally
        if len(week_boxes) + 1 > l1:
            return JsonResponse({'error': f'Total boxes added in a week cannot be more than {l1}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check the total boxes added in a week by a user condition
        user_week_boxes = user_boxes.filter(created_at__week=request.data['created_at'].isocalendar()[1])
        l2 = 50 # Default value, should be configured externally
        if len(user_week_boxes) + 1 > l2:
            return JsonResponse({'error': f'Total boxes added in a week by a user cannot be more than {l2}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return JsonResponse(serializer.data)
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete API
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_box(request, box_id):
    try:
        box = Box.objects.get(id=box_id)
    except Box.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.user == box.creator:
        box.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_403_FORBIDDEN)


# List all Api
@login_required
def box_list(request):
    # get all boxes
    boxes = Box.objects.all()

    # apply filters based on query parameters
    length_more_than = request.GET.get('length_more_than')
    length_less_than = request.GET.get('length_less_than')
    breadth_more_than = request.GET.get('breadth_more_than')
    breadth_less_than = request.GET.get('breadth_less_than')
    height_more_than = request.GET.get('height_more_than')
    height_less_than = request.GET.get('height_less_than')
    area_more_than = request.GET.get('area_more_than')
    area_less_than = request.GET.get('area_less_than')
    volume_more_than = request.GET.get('volume_more_than')
    volume_less_than = request.GET.get('volume_less_than')
    created_by = request.GET.get('created_by')
    created_before = request.GET.get('created_before')
    created_after = request.GET.get('created_after')

    if length_more_than:
        boxes = boxes.filter(length__gt=length_more_than)
    if length_less_than:
        boxes = boxes.filter(length__lt=length_less_than)
    if breadth_more_than:
        boxes = boxes.filter(breadth__gt=breadth_more_than)
    if breadth_less_than:
        boxes = boxes.filter(breadth__lt=breadth_less_than)
    if height_more_than:
        boxes = boxes.filter(height__gt=height_more_than)
    if height_less_than:
        boxes = boxes.filter(height__lt=height_less_than)
    if area_more_than:
        boxes = boxes.filter(area__gt=area_more_than)
    if area_less_than:
        boxes = boxes.filter(area__lt=area_less_than)
    if volume_more_than:
        boxes = boxes.filter(volume__gt=volume_more_than)
    if volume_less_than:
        boxes = boxes.filter(volume__lt=volume_less_than)
    if created_by:
        boxes = boxes.filter(created_by__username=created_by)
    if created_before:
        boxes = boxes.filter(created_at__lt=datetime.strptime(created_before, '%Y-%m-%d').date())
    if created_after:
        boxes = boxes.filter(created_at__gt=datetime.strptime(created_after, '%Y-%m-%d').date())

    # serialize the boxes
    serializer = BoxSerializer(boxes, many=True)

    # add additional fields for staff users
    if request.user.is_staff:
        serializer = serializer.fields + ('created_by', 'last_updated')

    return JsonResponse(serializer.data, safe=False)


# List my boxes:
@login_required
@require_GET
def list_my_boxes(request):
    user = request.user
    boxes = Box.objects.filter(created_by=user)
    
    length_more_than = request.GET.get('length_more_than')
    length_less_than = request.GET.get('length_less_than')
    breadth_more_than = request.GET.get('breadth_more_than')
    breadth_less_than = request.GET.get('breadth_less_than')
    height_more_than = request.GET.get('height_more_than')
    height_less_than = request.GET.get('height_less_than')
    area_more_than = request.GET.get('area_more_than')
    area_less_than = request.GET.get('area_less_than')
    volume_more_than = request.GET.get('volume_more_than')
    volume_less_than = request.GET.get('volume_less_than')

    if length_more_than:
        boxes = boxes.filter(length__gt=float(length_more_than))
    if length_less_than:
        boxes = boxes.filter(length__lt=float(length_less_than))
    if breadth_more_than:
        boxes = boxes.filter(breadth__gt=float(breadth_more_than))
    if breadth_less_than:
        boxes = boxes.filter(breadth__lt=float(breadth_less_than))
    if height_more_than:
        boxes = boxes.filter(height__gt=float(height_more_than))
    if height_less_than:
        boxes = boxes.filter(height__lt=float(height_less_than))
    if area_more_than:
        boxes = boxes.filter(area__gt=float(area_more_than))
    if area_less_than:
        boxes = boxes.filter(area__lt=float(area_less_than))
    if volume_more_than:
        boxes = boxes.filter(volume__gt=float(volume_more_than))
    if volume_less_than:
        boxes = boxes.filter(volume__lt=float(volume_less_than))

    serializer = BoxSerializer(boxes, many=True)

    return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def adminview(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)


def home(request):
    return render(request, "cuboidapp/base.html")