from rest_framework import generics, status
from rest_framework.response import Response


class UserView(generics.GenericAPIView):
    def get(self, request):
        return Response({"data": "Hello, World!"}, status=status.HTTP_200_OK)
