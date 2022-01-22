from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CauseSerializer
from .models import Cause


# Create your views here.

@api_view(['POST'])
def create_cause(request):
    serializer = CauseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_causes(request):
    causes = Cause.objects.all()
    serializer = CauseSerializer(instance=causes, many=True)
    return Response({'status': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)
