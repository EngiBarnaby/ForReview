from rest_framework import serializers




class SearchRequestSerializer(serializers.Serializer):
    psp = serializers.IntegerField(default=80, required=False, write_only=True)
    ex_mdls = serializers.ListSerializer(default=list(), required=False, write_only=True)
    rows = serializers.ListSerializer(required=True, write_only=True)



