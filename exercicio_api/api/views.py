# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import SentimentAnalysisSerializer, CartRecoverySerializer
from api.models.base import GroqClient, get_logger
from api.models.clientes import Clientes
from api.models.produtos import Produtos

log = get_logger(__name__)
groq_client = GroqClient()


class SentimentAnalysisView(APIView):
    """
    Análise de Sentimento de conversas do SAC.
    Exemplo de body: { "text": "O atendimento foi péssimo, muito demorado!" }
    """
    permission_classes = [IsAuthenticated]
    
    # Parâmetro manual do Bearer Token (para o "Authorize" do Swagger)
    bearer_token_param = openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Formato: Bearer <token>",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(
        operation_description="Análise de Sentimento de conversas do SAC",
        request_body=SentimentAnalysisSerializer,   # Mostra o body no Swagger
        manual_parameters=[bearer_token_param],     # Exibe campo de Authorization no header
        responses={
            200: openapi.Response("OK", SentimentAnalysisSerializer),
            400: "Bad Request",
        }
    )
    
    def post(self, request):
        serializer = SentimentAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            # Montamos um prompt específico para a Groq
            prompt = (
                f"Analise o sentimento do seguinte texto em português brasileiro de um cliente: '{text}'. "
                f"Retorne 'positivo', 'neutro' ou 'negativo'."
            )
            response_text = groq_client.send_prompt(prompt)
            log.info(f"Sentiment Analysis response: {response_text}")
            return Response({"sentiment": response_text}, status=status.HTTP_200_OK)
        else:
            log.warning("Dados inválidos para sentiment analysis.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartRecoveryView(APIView):
    """
    Geração de Copy para recuperação de carrinho abandonado.
    Exemplo de body: { "descricao_produto": "Smartphone X", 
                        "cliente_id":"1212", 
                        "nome_cliente": "Maria", "email": "nome@provedor.com"}
    """
    permission_classes = [IsAuthenticated]
    
    bearer_token_param = openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Formato: Bearer <token>",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(
        operation_description="Geração de Copy para recuperação de carrinho abandonado",
        request_body=CartRecoverySerializer,
        manual_parameters=[bearer_token_param],
        responses={
            200: "Texto gerado",
            400: "Bad Request"
        }
    )
    
    def post(self, request):
        serializer = CartRecoverySerializer(data=request.data)
        if serializer.is_valid():
            descricao_produto = serializer.validated_data['descricao_produto']
            cliente_id = serializer.validated_data['cliente_id']
            nome_cliente = serializer.validated_data.get('nome_cliente', 'Cliente')
            email = serializer.validated_data.get('email', 'Cliente')
            
            try:
                # 1. Buscar ou criar o cliente
                cliente, created = Clientes.objects.get_or_create(
                    id=cliente_id,
                    nome=nome_cliente,
                    email=email
                )
                # Se já existir um cliente com esse id, 'created' será False
                if not created and not cliente.nome and nome_cliente:
                    # Se quiser atualizar o nome caso esteja vazio
                    cliente.nome = nome_cliente
                    cliente.email = email
                    cliente.save()

                # 2. Criar produto relacionado ao cliente
                produto = Produtos.objects.create(
                    descricao=descricao_produto,
                    cliente=cliente # referência ao Customer
                )
            except IntegrityError as e:
                log.exception(f"Erro ao criar registro no banco.")
                return Response(
                    {
                        "detail": "Erro de integridade no banco de dados.",
                        "error": str(e)
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            log.info(f"NOme:{nome_cliente} - Email:{email} - Cliente:{cliente} - Produto:{produto}")
            prompt = (
                f"Crie um texto persuasivo em português brasileiro para {nome_cliente} que deixou o {descricao_produto} "
                f"no carrinho. O tom deve ser amigável e enfatizar a urgência da compra, cite sempre o nome do cliente e do produto,"
                f"gere o link do carrinho (base da url: https:www.zenirmoveis.com.br/url_do_carrinho) "
                f"e sugira um cupom de desconto de 5% chamado ZENIR5 para finalizar a compra."
            )
            response_text = groq_client.send_prompt(prompt)
            log.info(f"Cart Recovery response: {response_text}")
            return Response({
                "copy_text": response_text, 
                "cliente_id": cliente.id,
                "produto_id": produto.id
                }, status=status.HTTP_200_OK)
        else:
            log.warning("Dados inválidos para cart recovery.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
