import os
import random
import string
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import datetime
        
class Usuario(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f"Usario {self.email}"

def file_model_path(instance, filename):
    return f"{instance.tipo_de_documento}/{filename}"

def image_upload(instance, filename):
    return f"Obra/{instance.id}/{filename}"

class Obra(models.Model):
    nombre = models.CharField(max_length=200)
    supervisor=models.CharField(max_length=100)
    contratista_fiscal=models.CharField(max_length=100)
    num_contrato=models.CharField(max_length=50, unique=True)
    imagen = models.ImageField(upload_to=image_upload, null=True)
    semanas=models.ManyToManyField("Semana", related_name="obra_week", blank=True)
    
    def __str__(self):
        return f"{self.nombre}"
    
    def delete(self):
        files = self.semanas.all()
        if files:
            for file in files:
                file.delete()
        super(Semana, self).delete()
    def save(self, *args, **kwargs):
        super(Obra, self).save(*args, **kwargs) 
        for semana in self.semanas.all():
            if not semana.cumplimiento_general:
                semana.cumplimiento_general=semana.cumplimiento_general_function()
                semana.save()
        super(Obra, self).save(*args, **kwargs)    
class Semana(models.Model):
    indicadores=models.ManyToManyField("Valor_Indicador", related_name="semana_indicador",blank=True)
    num_semana=models.IntegerField(null=True, blank=True)
    cumplimiento_general=models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    documentos=models.ManyToManyField("Documento", related_name="week_doc", blank=True)
    mes=models.IntegerField(null=True, blank=True)
    año=models.IntegerField(null=True, blank=True)
    class Meta:
       ordering = ['año', 'num_semana']
    def __str__(self):
        obra=self.obra_week.first()
        return f"{obra} {self.num_semana} - {self.año}"

    def cumplimiento_general_function(self):
        print(self.indicadores.all())
        l=[n.valor for n in self.indicadores.all()]
        print(l)
        print(sum(l))
        print(len(l))
        return sum(l)/len(l)

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            date_now=timezone.now().date()
            self.num_semana=date_now.isocalendar()[1]
            self.mes=date_now.month
            self.año=date_now.year
            super(Semana, self).save(*args, **kwargs)
        else:
            self.cumplimiento_general=self.cumplimiento_general_function()
            super(Semana, self).save(*args, **kwargs)
        self.cumplimiento_general=self.cumplimiento_general_function()
        super(Semana, self).save(*args, **kwargs)    
    def delete(self):
        files = self.documentos.all()
        if files:
            for file in files:
                file.delete()
        super(Semana, self).delete()
    def serialize(self):
        return{
            "id":self.id,
            "indicadores":[i.serialize() for i in self.indicadores.all()],
            "cumplimiento_general":self.cumplimiento_general,
            "num_semana":self.num_semana
        }
class Documento(models.Model):
    ACTA_CAMPO="Acta de Campo"
    ACTA_CONFORMIDAD="Acta de Conformidad"
    OTROS="Otros"
    element_types=(
        (ACTA_CAMPO, "Acta de Campo"),
        (ACTA_CONFORMIDAD, "Acta de Conformidad"),
        (OTROS, "Otros"),
    )
    file=models.FileField(upload_to=file_model_path)
    tipo_de_documento=models.CharField(max_length=100, choices=element_types, default=OTROS)
    def serialize(self):
        return {
            "id":self.id,
            "tipo_de_documento":self.tipo_de_documento,
            "filename": os.path.basename(self.file.name),
            "url": self.file.url
        }
    def __str__(self):
        return f"{self.file}"

class Indicadores(models.Model):
    nombre=models.CharField(max_length=100)
    ponderacion=models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"Indicador {self.nombre}"

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ponderacion":self.ponderacion
        }
class Valor_Indicador(models.Model):
    valor=models.DecimalField(default=0, max_digits=5, decimal_places=2)
    indicador=models.ForeignKey(Indicadores, on_delete=models.CASCADE, related_name="vindicador_indicador")
    
    def __str__(self):
        return f"{self.indicador.nombre}: {self.valor}"
    
    def puntuacion(self):
        valor=round(self.valor, 2)
        return valor


    def serialize(self):
        return {
            "id": self.id,
            "valor": self.valor,
            "indicador":self.indicador.serialize()
        }
    def save(self, *args, **kwargs):
        super(Valor_Indicador, self).save(*args, **kwargs)
        try:
            week=self.semana_indicador.first()
            week.cumplimiento_general=week.cumplimiento_general_function()
            week.save()
        except:
            pass