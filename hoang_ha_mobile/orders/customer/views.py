from rest_framework_simplejwt import authentication
from rest_framework import generics, permissions, response, status
from rest_framework import filters

from variants.models import Variant
from . import serializers
from .. import models

from hoang_ha_mobile.base.errors.errors import check_valid_item
from hoang_ha_mobile.base.errors.bases import return_code_400
from hoang_ha_mobile.base.services.payments.stripe.views \
import create_payment_intent



class ListCreateOrderAPIView(generics.ListCreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderReadSerializer
    filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['-created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):        
        self.queryset = models.Order.objects.filter(created_by=self.request.user.id)
        return super().get_queryset()    
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderSerializer(data=request.data.get('order'))   
        array_order_detail = self.request.data.get("order_details")
        temp = check_valid_item(array_order_detail)        
        if(temp is not None):
            return temp
        
        if(serializer.is_valid()):            
            self.instance = serializer.save(created_by=self.request.user)
            instance_price = 0            
            # if(len(array_order_detail) < 1): 
            #     return response.Response(data={"Error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            # for order_detail in array_order_detail:
            #     if not (int(order_detail.get('quantity')) > 0): 
            #         return response.Response(data={"Error: Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
            #     try:
            #         variant = Variant.objects.get(id=order_detail.get('variant'))
            #     except:
            #         return response.Response(data={"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            temp = check_valid_item(array_order_detail)
            if(temp is not None):
                return temp
            
            for order_detail in array_order_detail:       
                variant = Variant.objects.get(id=order_detail.get('variant'))
                if(variant.sale > 0):
                    price = variant.sale
                else:
                    price = variant.price
                    
                instance_price += int(price) * int(order_detail.get('quantity'))
                data = {
                    "order": self.instance.id,
                    "variant": order_detail.get('variant'),
                    "quantity": order_detail.get('quantity'),
                    "price": price
                }
                serializer = serializers.OrderDetailSerializer(data=data)
                if(serializer.is_valid()):
                    serializer.save()
                    
            self.instance.total = instance_price
            self.instance.save()
            # print(self.instance)
            # serializer = self.get_serializer(self.instance)
            serializer = serializers.OrderSerializer(self.instance)            
            payment_method_id = self.request.data.get("payment_method_id")            
            data_t = create_payment_intent(serializer.data['email'], serializer.data['total'], serializer.data['id'], payment_method_id, self.request.user.id)            
            if(data_t['status'] == "charge"):
                self.instance.charge_id = data_t['data'].charges.data[0].id
                self.instance.save()
            
            serializer = self.get_serializer(self.instance)
            if(data_t['status'] == False):
                message = data_t['data']
                data_return = {
                    "message": message,
                    "charge": False,
                    "data": serializer.data
                }
            else:                
                data_return = {
                    "message": "Order successfully",
                    "charge": True,
                    "data": serializer.data
                }
            
            
            # if(data_t['status'] == False):
            #     message = data_t['data']
            #     return return_code_400(message)
                
            # data_return = {
            #     "message": "Order successfully",
            #     "data": serializer.data
            # }
            
            # return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return response.Response(data=data_return, status=status.HTTP_201_CREATED)        
        else:            
            return response.Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


