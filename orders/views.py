from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .cart import Cart
from products.models import Product
from .serializers import AddProductSerializer, CartSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        cart = Cart(request)
        serializer_data = CartSerializer(instance=cart, many=True)
        return Response(data=serializer_data.data, status=status.HTTP_200_OK)


class CartAddView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id )
        ser_data = AddProductSerializer(data=request.data)
        if ser_data.is_valid():

            try:
                with transaction.atomic():

                    quantity_to_add = ser_data.validated_data['quantity']
                    if product.inventory < quantity_to_add:
                        return Response({'message': 'Not enough stock available'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    cart.add(product, ser_data.validated_data['quantity'], user=request.user)
                    product.inventory -= quantity_to_add
                    product.save()
                    return Response({'messages': 'product added to cart'},
                                    status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': 'an error while transaction, call contact'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
