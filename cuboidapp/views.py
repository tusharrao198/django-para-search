from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Box
from .serializers import BoxSerializer, BoxlistAllSerializer, BoxlistAllSerializerisStaff


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

    # print(data, "\n", user)
    
    # Check if user has exceeded the limit of boxes added in a week
    week_ago = timezone.now() - timedelta(days=7)
    boxes_added_this_week = Box.objects.filter(created_by=user, created_at__gte=week_ago).count()
    if boxes_added_this_week >= L2:
        return Response({'error': 'User has exceeded the limit of boxes added in a week.'}, status=400)
    
    serializer = BoxSerializer(data=data)
    if serializer.is_valid():
        # Check if average area and volume of all boxes do not exceed their limits
        all_boxes = Box.objects.all()
        cnt =all_boxes.count()
        all_boxes_area = sum([box.length * box.breadth for box in all_boxes])
        all_boxes_volume = sum([box.length * box.breadth * box.height for box in all_boxes])
        new_box_area = data['length'] * data['breadth']
        new_box_volume = data['length'] * data['breadth'] * data['height']

        if (all_boxes_area + new_box_area) / (cnt + 1) > A1:
            return Response({'error': 'Average area of all boxes exceed limit.'}, status=400)
        if (all_boxes_volume + new_box_volume) / (cnt + 1) > V1:
            return Response({'error': 'Average volume of all boxes exceed limit.'}, status=400)
        
        # Create and save the new box
        serializer.save(created_by=user)
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)


# Delete API
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_box(request, box_id):
    try:
        box = Box.objects.get(id=box_id)
    except Box.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.user == box.created_by:
        box.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_403_FORBIDDEN)


# Update API
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_box(request, box_id):
    if request.data.get('created_by') is not None:
        return Response({'error': 'Cannot Change Creator, Remove the created_by key from request body'}, status=400)

    try:
        box = Box.objects.get(id=box_id)
    except Box.DoesNotExist:
        return Response({'error': 'Box not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.is_staff:
        creator = box.created_by
    else:
        creator = request.user
    
    # Check if the user has permission to update the box
    if not request.user.is_staff and creator != request.user:
        return Response({'error': 'You do not have permission to update this box'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check if the update is allowed based on the new dimensions and the average area condition
    all_boxes = Box.objects.all()
    cnt = Box.objects.all().count()        
    all_boxes_area = sum([box.length * box.breadth for box in all_boxes])
    

    new_area_sum = (all_boxes_area - (box.length * box.breadth) + request.data['length'] * request.data['breadth'])
    if (new_area_sum) / cnt > A1:
        return Response({'error': f'Average area of all added boxes should not exceed {A1}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the update is allowed based on the new dimensions and the average volume condition

    user_boxes = Box.objects.filter(created_by=creator)
    user_boxes_cnt = Box.objects.filter(created_by=creator).count()
    user_boxes_volume = sum([box.length * box.breadth * box.height for box in user_boxes])

    new_volume_sum = (user_boxes_volume - (box.length * box.breadth * box.height) + request.data['length'] * request.data['breadth'] * request.data['height'])

    if (new_volume_sum) / (user_boxes_cnt) > V1:
        return Response({'error': 'Average volume of all boxes added by you should not exceed {}'.format(V1)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the update is allowed based on the total boxes added in a week condition
    if Box.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count() > L1:
        return Response({'error': f'Total Boxes added in a week cannot be more than {L1}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the update is allowed based on the total boxes added in a week by a user condition
    if Box.objects.filter(created_by=creator, created_at__gte=timezone.now() - timezone.timedelta(days=7)).count() > L2:
        return Response({'error': f'Total Boxes added in a week by you cannot be more than {L2}'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = BoxlistAllSerializerisStaff(box, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save(modified_at=datetime.now())
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all Api
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


    # add additional fields for staff users
    if request.user.is_staff:
        # serialize the boxes
        serializer = BoxlistAllSerializerisStaff(boxes, many=True)
    else:
        # serialize the boxes
        serializer = BoxlistAllSerializer(boxes, many=True)         

    return JsonResponse(serializer.data, safe=False)


# List my boxes:
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
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

    if request.user.is_staff:
        # serialize the boxes
        serializer = BoxlistAllSerializerisStaff(boxes, many=True)
        # serializer = BoxSerializer(boxes, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return Response({'error': f'Sorry, {request.user}, Only Staff user can see his/her created boxes in the store'}, status=status.HTTP_400_BAD_REQUEST)

