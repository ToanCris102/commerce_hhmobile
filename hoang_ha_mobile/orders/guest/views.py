from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from hoang_ha_mobile.base.errors.errors import check_valid_item
from hoang_ha_mobile.base.errors.bases import return_code_400
from hoang_ha_mobile.base.services.payments.stripe.views \
import create_payment_intent

from variants.models import Variant
from .serializers import OrderSerializer, OrderDetailSerializer, ListOrderSerializer
from ..models import Order



class CreateOrderApiView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        self.queryset = Order.objects.filter(
            email=self.request.query_params.get('email').lower()).prefetch_related()
        return super().get_queryset()

    def get_serializer(self, *args, **kwargs):
        if(self.request.method == "POST"):
            return super().get_serializer(*args, **kwargs)
        return ListOrderSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['order']['email'] = request.data['order'].get(
            'email').lower()

        order_detail = self.request.data.get("order_details")
        items = check_valid_item(order_detail)
        if(items is not None):
            return items

        serializer = OrderSerializer(data=request.data.get('order'))
        if(serializer.is_valid()):
            self.instance = serializer.save()
            total = 0
            for data in order_detail:
                variant = Variant.objects.get(id=data.get(
                    'variant'), status=True, deleted_by=None)
                if variant.sale:
                    price = variant.sale
                    total += int(variant.sale) * int(data.get('quantity'))
                else:
                    price = variant.price
                    total += int(variant.price) * int(data.get('quantity'))
                data_save = {
                    "order": self.instance.id,
                    "variant": data.get('variant'),
                    "quantity": data.get('quantity'),
                    "price": price
                }
                serializer = OrderDetailSerializer(data=data_save)
                if(serializer.is_valid()):
                    serializer.save()
            self.instance.total = total
            self.instance.save()  
            # serializer = self.get_serializer(self.instance)          
            payment_method_id = self.request.data.get("payment_method_id")  
            # data_t = create_payment_intent(serializer.data['email'], serializer.data['total'], serializer.data['id'], payment_method_id, account_id=None)
            data_t = create_payment_intent(self.instance.email, self.instance.total, self.instance.id, payment_method_id, account_id=None)
            if(data_t['status'] == "charge"):
                self.instance.charge_id = data_t['data'].charges.data[0].id
                self.instance.save()
            
            serializer = self.get_serializer(self.instance)
            if(data_t['status'] == False):
                message = data_t['data']
                data_return = {
                    "message": message,
                    "data": serializer.data
                }
            else:                
                data_return = {
                    "message": "Order successfully",
                    "data": serializer.data
                }
            
            return Response(data=data_return, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class OrderDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related()
    lookup_url_kwarg = "order_id"

    def update(self, request, *args, **kwargs):
        data = get_object_or_404(Order, id=self.kwargs['order_id'])
        if data.status == "processing":
            serializer = self.get_serializer(
                data, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(data=serializer.data)
        else:
            return Response(data={"message": "Not Update!"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


