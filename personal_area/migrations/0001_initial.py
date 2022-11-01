# Generated by Django 4.0.5 on 2022-06-16 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('house', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.IntegerField(null=True)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('decision_time', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppealCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('patronymic', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=255)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.address')),
            ],
        ),
        migrations.CreateModel(
            name='BenefitCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ConsiderationStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Deputy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('patronymic', models.CharField(max_length=255)),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.constituency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('photo', models.ImageField(null=True, upload_to='photos/')),
                ('cover', models.ImageField(null=True, upload_to='photos/')),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SocialStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('appeal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.appeal')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.applicant')),
                ('deputy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.deputy')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.sender')),
            ],
        ),
        migrations.AddField(
            model_name='applicant',
            name='benefit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='personal_area.benefitcategory'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='social_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.socialstatus'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.applicant'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.appealcategory'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='consideration_stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.considerationstage'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='decision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.decision'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='responsible_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.deputy'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_area.topic'),
        ),
    ]