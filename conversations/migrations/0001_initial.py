# Generated by Django 3.1.1 on 2020-10-10 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0002_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_msg', to='conversations.chat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.profile')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ChatMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_viewed', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='conversations.chat')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='pages.profile')),
            ],
        ),
    ]
