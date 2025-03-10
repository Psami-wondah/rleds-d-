from unicodedata import category
from rest_framework import serializers
from .models import Apartment
from django.db.models.base import ModelState
from django.db import models

class ApartmentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ApartmentSerializer, self).__init__(*args, **kwargs)
    class Meta:
        model = Apartment
        fields = ['apartment_id', 'name','category', 'image', 'price', 'location', 'agent']


class ApartmentSearchSerializer(serializers.Serializer):
    location = serializers.CharField()
    price_range = serializers.CharField()
    category = serializers.CharField()

    def __strr__(self):
        return self.category