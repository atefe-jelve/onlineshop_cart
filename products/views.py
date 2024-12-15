from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ListProduct(APIView):
    permission_classes = [IsAuthenticated, ]
    query_set = Product.objects.all()

    def get(self, request):
            serializer_data = ProductSerializer(instance=self.query_set, many=True)
            return Response(data=serializer_data.data)
