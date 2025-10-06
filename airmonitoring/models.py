from django.db import models

# Por ahora lo dejamos simple, después agregamos más campos
class Busqueda(models.Model):
    ciudad = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ciudad