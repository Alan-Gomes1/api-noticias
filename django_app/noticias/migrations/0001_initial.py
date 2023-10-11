# Generated by Django 4.2.6 on 2023-10-09 14:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noticias',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255)),
                ('conteudo', models.TextField()),
                ('autor', models.CharField(max_length=255)),
                ('publicado', models.BooleanField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]