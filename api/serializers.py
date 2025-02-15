# api/serializers.py
from rest_framework import serializers

class SentimentAnalysisSerializer(serializers.Serializer):
    text = serializers.CharField()

class CartRecoverySerializer(serializers.Serializer):
    descricao_produto = serializers.CharField()
    cliente_id = serializers.CharField(required=True)
    nome_cliente = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

