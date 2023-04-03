# Generated by Django 4.0.4 on 2022-12-15 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_documento_element_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='element_type',
            new_name='tipo_de_documento',
        ),
        migrations.RemoveField(
            model_name='semana',
            name='Acta_de_Campo',
        ),
        migrations.RemoveField(
            model_name='semana',
            name='Acta_de_Inconformidad',
        ),
        migrations.RemoveField(
            model_name='semana',
            name='Otros',
        ),
        migrations.AddField(
            model_name='documento',
            name='semana',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doc_week', to='home.semana'),
        ),
    ]