from django.shortcuts import get_object_or_404
from rest_framework import serializers

def get_model_from_dict_or_uuid(serializer, model, data):
    if isinstance(data, dict):
        if "uuid" in data:
            model_to_edit = get_object_or_404(model, uuid=data.get('uuid'))
            serialized_data = serializer(model_to_edit, data=data)
        else:
            serialized_data = serializer(data=data)
        if serialized_data.is_valid(raise_exception=True):
            return serialized_data.save()
        else:
            raise serializers.ValidationError(serializer.errors)
    else:
        return get_object_or_404(model, uuid=data)