# api/models/clientes.py
from django.db import models

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    

    def __str__(self):
        return f"(id={self.id}) - {self.nome}"
