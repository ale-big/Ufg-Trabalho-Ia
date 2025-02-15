# api/models/produtos.py
from django.db import models
from api.models.clientes import Clientes 

class Produtos(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_compra = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.descricao
