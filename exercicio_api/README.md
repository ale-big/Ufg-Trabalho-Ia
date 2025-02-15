# Projeto de IA para atendimento do SAC

API desenvolvida em **Django + Django Rest Framework**, utilizando **Groq** como LLM para:
1. **Análise de Sentimento** (texto do SAC)
2. **Geração de Copy** para recuperação de carrinho abandonado

## Pré-requisitos

- Python 3.x
- Virtualenv (opcional)
- Dependências listadas em `requirements.txt`

## Configuração

1. **Clone este repositório**.
2. **Crie um arquivo `.env`** na raiz do projeto com:
GROQ_API_KEY="sua_chave_groq_aqui"

3. **Instale as dependências**:
``bash
pip install -r requirements.txt
`
4. **Execute as migrações**:
``bash
python manage.py migrate
``
5. **Inicie o servidor**:
``bash
python manage.py runserver
``

## Uso

- **Acesse /swagger/ para visualizar e testar os endpoints (documentação via drf_yasg)**.
Autentique-se em /api/token/ (JWT).
Utilize as rotas /api/v1/sentiment/ e /api/v1/cart-recovery/.
Exemplo de Teste via cURL


- **Gerar Token JWT**

``bash
curl -X POST -H "Content-Type: application/json" \
-d '{"username":"seuuser","password":"seusenha"}' \
http://127.0.0.1:8000/api/token/
``

O retorno será um JSON com access e refresh. Utilize o access token como Bearer Token.

- **Análise de Sentimento**

``bash
curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer <SUA_TOKEN_AQUI>" \
-d '{"text":"Eu adorei o suporte, muito rápido e eficiente!"}' \
http://127.0.0.1:8000/api/v1/sentiment/
``

Exemplo de retorno (JSON):
``json
{
  "sentiment": "positivo"
}
``

- **Geração de Copy de Recuperação de Carrinho**

``bash
curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer <SUA_TOKEN_AQUI>" \
-d '{"product_name":"Notebook Gamer"}' \
http://127.0.0.1:8000/api/v1/cart-recovery/
``

Exemplo de retorno (JSON):
``json
{
  "copy_text": "Olá, Cliente! Percebemos que você..."
}
``

