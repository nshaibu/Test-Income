from rest_framework.response import Response
from rest_framework import generics, status

from .serializers import InputSerializer


class UserSalaryDetailView(generics.CreateAPIView):
    serializer_class = InputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(instance.to_dict(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
