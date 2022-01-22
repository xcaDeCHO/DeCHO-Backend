from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CauseSerializer


# Create your views here.

@api_view(['POST'])
def create_cause(request):
    serializer = CauseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data}, status=status.HTTP_201_CREATED)
