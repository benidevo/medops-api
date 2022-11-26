from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from apps.users.serializers.account import UserAccountSerializer
from services import Cache
from utils.response import Response


class UserAccountView(generics.GenericAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = get_user_model()
    cache = Cache()

    def get(self, request):
        user = self.model.objects.filter(id=request.user.id).first()
        serializer = self.get_serializer(user)
        return Response(
            success=True,
            message="Retrieved user account",
            data=serializer.data,
            status_code=200,
        )

    def patch(self, request):
        user = self.model.objects.filter(id=request.user.id).first()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                success=False,
                data=serializer.errors,
                status_code=400,
            )
        serializer.save()

        return Response(
            success=True,
            message="User account updated",
            data=serializer.data,
            status_code=200,
        )

    def delete(self, request):
        user = self.model.objects.filter(id=request.user.id).first()
        if user:
            user.delete()

        return Response(success=True, message="Account deleted", status_code=200)
