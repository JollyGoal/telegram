from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class ButtonView(APIView):
    def get(self, request):
        users = Button.objects.all()
        serializer = ButtonSerializer(users, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        pass


class TextView(APIView):
    def get(self, request):
        texts = Text.objects.all()
        serializer = TextSerializer(texts, many=True)
        return Response({'data': serializer.data})



