from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .cart import Cart
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from .serializers import AddProductSerializer, CartSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        cart = Cart(request)
        serializer_data = CartSerializer(instance=cart, many=True)
        return Response(data=serializer_data.data, status=status.HTTP_200_OK)


class CartAddView(APIView):
    def post(self, request, product_id):
        card = Cart(request)
        product = get_object_or_404(Product, id=product_id )
        ser_data = AddProductSerializer(data=request.data)
        if ser_data.is_valid():
            quantity_to_add = ser_data.validated_data['quantity']
            if product.inventory < quantity_to_add:
                return Response({'message': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)

            card.add(product, ser_data.validated_data['quantity'])
            product.inventory -= quantity_to_add
            product.save()
            return Response({'messages': 'product added to cart'}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
