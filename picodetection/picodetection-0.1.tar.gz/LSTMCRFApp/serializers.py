from rest_framework import serializers

class OutPutSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   #Input = serializers.JSONField()
   Output = serializers.JSONField()
