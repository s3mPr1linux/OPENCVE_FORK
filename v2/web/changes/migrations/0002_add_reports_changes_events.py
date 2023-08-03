# Generated by Django 4.2.3 on 2023-08-02 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('cves', '0001_initial'),
        ('changes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='projects.project'),
        ),
        migrations.AddField(
            model_name='event',
            name='change',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='changes.change'),
        ),
        migrations.AddField(
            model_name='event',
            name='cve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='cves.cve'),
        ),
        migrations.AddField(
            model_name='change',
            name='cve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='cves.cve'),
        ),
        migrations.AddConstraint(
            model_name='report',
            constraint=models.UniqueConstraint(fields=('created_at', 'project_id'), name='ix_unique_project_created_at'),
        ),
    ]