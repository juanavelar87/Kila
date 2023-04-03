from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("obra/<int:id>", views.individual, name="individual"),
    path("obra/<int:id>/documentos", views.obra_documents, name="obra_documents"),
    path("obra/<int:id>/report", views.report, name="week_report")
]
