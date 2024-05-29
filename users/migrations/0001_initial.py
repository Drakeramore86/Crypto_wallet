from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('short_intro', models.CharField(blank=True, max_length=200, null=True)),
                ('account_photo', models.ImageField(blank=True, default='profiles/default.png', null=True, upload_to='profiles/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_profile',  # Add this line to specify the existing table name
            },
        ),
    ]