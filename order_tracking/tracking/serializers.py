from rest_framework import serializers
from .models import *
from rest_framework.serializers import HyperlinkedIdentityField,ModelSerializer



order_detail_url = HyperlinkedIdentityField(view_name='home:details',lookup_field="id")
class PlaceSerializer(serializers.ModelSerializer):
    url=order_detail_url
    class Meta:
        model = Order
        fields="__all__"
        extra_kwargs={"user":{"read_only":True},"ordered":{"read_only":True}}


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields="__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["order"].queryset = Order.objects.filter(ordered=False)

order_update_url = HyperlinkedIdentityField(view_name='home:update',lookup_field="id")
class OrderUpdateSerializer(serializers.ModelSerializer):
    url=order_update_url
    class Meta:
        model = Driver
        fields="__all__"
        extra_kwargs={"order":{"read_only":True}}


