# Generated by Django 3.1.1 on 2020-09-11 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('path', models.CharField(max_length=128)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('path', models.CharField(max_length=128, unique=True)),
                ('delete_on_process', models.BooleanField(default=False)),
                ('container_type', models.IntegerField(choices=[(0, 'Input'), (1, 'Output'), (2, 'Structural')], default=2)),
                ('notes', models.TextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('parent_container', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_containers', to='assets.assetcontainer')),
            ],
        ),
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('type_code', models.CharField(blank=True, max_length=12, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransformerArchetype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('notes', models.TextField(blank=True, null=True)),
                ('transformer_type', models.IntegerField(choices=[(1, 'File'), (2, 'Directory')])),
                ('transformer_automations', models.IntegerField(choices=[(0, 'Automatic'), (1, 'Manual'), (2, 'Automaicic On Approval'), (3, 'Manual On Approval')])),
                ('validation_script', models.TextField(blank=True, null=True)),
                ('transformation_script', models.TextField(blank=True, null=True)),
                ('cleanup_script', models.TextField(blank=True, null=True)),
                ('notification_script', models.TextField(blank=True, null=True)),
                ('script_variables', models.TextField(default='{"input","container","output","container"}')),
                ('media_type', models.ManyToManyField(related_name='transformer_archetypes', to='assets.MediaType')),
            ],
        ),
        migrations.CreateModel(
            name='TransFormer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_on_process', models.BooleanField(default=False)),
                ('script_variables', models.TextField(default='{"input","container","output","container"}')),
                ('input_containers', models.ManyToManyField(related_name='input_transformers', to='assets.AssetContainer')),
                ('media_type', models.ManyToManyField(related_name='transformer', to='assets.MediaType')),
                ('output_containers', models.ManyToManyField(related_name='output_transformers', to='assets.AssetContainer')),
                ('transformer_archetype', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transformers', to='assets.transformerarchetype')),
            ],
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prepared', models.DateTimeField(auto_created=True)),
                ('script_variables', models.TextField(default='{"input","container","output","container"}')),
                ('status', models.IntegerField(choices=[(0, 'Preparing'), (1, 'Pending'), (2, 'Paused'), (3, 'Succeeded'), (4, 'Failed')])),
                ('notes', models.TextField(blank=True, null=True)),
                ('pending_start', models.DateTimeField(null=True)),
                ('pending_end', models.DateTimeField(null=True)),
                ('finished_time', models.DateTimeField(null=True)),
                ('paused_time', models.DateTimeField(null=True)),
                ('input_assets', models.ManyToManyField(related_name='jobs_input', to='assets.Asset')),
                ('input_container', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobs', to='assets.assetcontainer')),
                ('output_containers', models.ManyToManyField(related_name='job_outputs', to='assets.AssetContainer')),
                ('output_paths', models.ManyToManyField(related_name='jobs_output', to='assets.Asset')),
                ('transformer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='assets.transformer')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='assets.assetcontainer'),
        ),
        migrations.AddField(
            model_name='asset',
            name='media_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assets', to='assets.mediatype'),
        ),
    ]
