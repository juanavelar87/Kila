import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from statistics import mean 
from .models import Documento, Obra
@login_required
def index(request):
    obras= reversed(Obra.objects.all())
    return render(request, "home/index.html",{
        "obras":obras
    })
    
@login_required
def individual(request, id):
    obra=Obra.objects.get(id=id)
    return render(request, "home/individual.html",{
        "Documento":Documento,
        "obra":obra
    })

@login_required
def report(request, id):
    if request.method=="GET":
        try:
            obra=Obra.objects.get(id=int(id))
            if request.GET["type"] == "week":
                week = obra.semanas.get(id=int(request.GET["type_id"]))
                return JsonResponse(week.serialize())
            elif request.GET["type"] == "month":
                monthly_report={}
                for week in obra.semanas.all():
                    try:
                        monthly_report[week.mes].append(week.cumplimiento_general)
                    except KeyError:
                        monthly_report[week.mes]=[week.cumplimiento_general]
                for key, value in monthly_report.items():
                    monthly_report[key]=round(mean(value),2)
                return JsonResponse(monthly_report, safe=False)
        except:
            pass

@login_required
def obra_documents(request, id):
    obra=Obra.objects.get(id=id)
    semanas=obra.semanas.exclude(documentos=None)
    documentos=[]
    for semana in semanas:
        documentos.append({
        "semana":f"Semana {semana.num_semana} - {semana.año}",
        "documentos":[documento.serialize() for documento in semana.documentos.all()]
        })
    return JsonResponse(documentos, status=200, safe=False)

