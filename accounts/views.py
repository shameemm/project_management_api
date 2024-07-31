from .serializers import UserSerializers
from .permissions import IsAdminOrManager
from rest_framework.views import APIView,Response
from rest_framework import status
# Create your views here.

class UserRegistrationView(APIView):
    """This will do the creation of user"""
    permission_classes = [IsAdminOrManager]
    def post(self,request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)