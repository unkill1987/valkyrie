# Generated by Django 2.1.3 on 2019-01-03 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('user_role', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Contract_BL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractname', models.CharField(max_length=50)),
                ('contract_id', models.CharField(max_length=20)),
                ('sha256', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('share1', models.CharField(max_length=100)),
                ('share2', models.CharField(max_length=100)),
                ('share3', models.CharField(max_length=100)),
                ('share4', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contract_CI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractname', models.CharField(max_length=50)),
                ('contract_id', models.CharField(max_length=20)),
                ('sha256', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('share1', models.CharField(max_length=100)),
                ('share2', models.CharField(max_length=100)),
                ('share3', models.CharField(max_length=100)),
                ('share4', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contract_DO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractname', models.CharField(max_length=50)),
                ('contract_id', models.CharField(max_length=20)),
                ('sha256', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('share1', models.CharField(max_length=100)),
                ('share2', models.CharField(max_length=100)),
                ('share3', models.CharField(max_length=100)),
                ('share4', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contract_LC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractname', models.CharField(max_length=50)),
                ('contract_id', models.CharField(max_length=20)),
                ('sha256', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('share1', models.CharField(max_length=100)),
                ('share2', models.CharField(max_length=100)),
                ('share3', models.CharField(max_length=100)),
                ('share4', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contract_LCR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractname', models.CharField(max_length=50)),
                ('contract_id', models.CharField(max_length=20)),
                ('sha256', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('share1', models.CharField(max_length=100)),
                ('share2', models.CharField(max_length=100)),
                ('share3', models.CharField(max_length=100)),
                ('share4', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contract_SR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractname', models.CharField(max_length=50)),
                ('contract_id', models.CharField(max_length=20)),
                ('sha256', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('share1', models.CharField(max_length=100)),
                ('share2', models.CharField(max_length=100)),
                ('share3', models.CharField(max_length=100)),
                ('share4', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_role', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('otpkey', models.CharField(max_length=20)),
                ('user_pw', models.CharField(max_length=20)),
                ('c_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=5000)),
                ('c_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_id', models.CharField(max_length=20)),
                ('CI_hash', models.CharField(max_length=100)),
                ('SR_hash', models.CharField(max_length=100)),
                ('LCR_hash', models.CharField(max_length=100)),
                ('LC_hash', models.CharField(max_length=100)),
                ('BL_hash', models.CharField(max_length=100)),
                ('DO_hash', models.CharField(max_length=100)),
                ('user1', models.CharField(max_length=50)),
                ('user2', models.CharField(max_length=50)),
                ('user3', models.CharField(max_length=50)),
                ('user4', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Process_complete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_id', models.CharField(max_length=20)),
                ('CI_hash', models.CharField(max_length=100)),
                ('SR_hash', models.CharField(max_length=100)),
                ('LCR_hash', models.CharField(max_length=100)),
                ('LC_hash', models.CharField(max_length=100)),
                ('BL_hash', models.CharField(max_length=100)),
                ('DO_hash', models.CharField(max_length=100)),
                ('user1', models.CharField(max_length=50)),
                ('user2', models.CharField(max_length=50)),
                ('user3', models.CharField(max_length=50)),
                ('user4', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='contract_sr',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='contract_lcr',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='contract_lc',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='contract_do',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='contract_ci',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='contract_bl',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
    ]
