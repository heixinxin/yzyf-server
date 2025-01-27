# Generated by Django 2.1.7 on 2019-08-25 17:00

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('alipay', models.CharField(default='', max_length=20, verbose_name='支付宝账号')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='电话号码')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=10)),
                ('userAdmin', models.BooleanField(default=False, verbose_name='商家验证')),
                ('perAdmin', models.BooleanField(default=False, verbose_name='个人验证')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'verbose_name': '用户信息',
                'db_table': 'yz_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ApplyJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(default='', max_length=10, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=10)),
                ('age', models.IntegerField(default='', verbose_name='年龄')),
                ('card_id', models.CharField(default='', max_length=30, verbose_name='身份证')),
                ('number', models.CharField(default='', max_length=11, verbose_name='电话号码')),
                ('status', models.SmallIntegerField(default=1, verbose_name='申请状态')),
            ],
            options={
                'verbose_name_plural': '申请信息',
                'verbose_name': '申请信息',
                'db_table': 'yz_apply',
            },
        ),
        migrations.CreateModel(
            name='HomeJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(default='', max_length=100, verbose_name='岗位名称')),
                ('price', models.CharField(default='10', max_length=50, verbose_name='报酬金额')),
                ('company', models.CharField(default='', max_length=100, verbose_name='公司名称')),
                ('place', models.CharField(default='', max_length=20, verbose_name='地点')),
                ('job_require', models.CharField(default='', max_length=500, verbose_name='工作要求')),
                ('company_info', models.CharField(default='', max_length=500, verbose_name='公司介绍')),
                ('eat', models.BooleanField(default=True)),
                ('live', models.BooleanField(default=True)),
                ('job_number', models.IntegerField(default=0, verbose_name='招收人数')),
                ('job_number_count', models.IntegerField(default=0, verbose_name='现有人数')),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='homejob', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '兼职信息',
                'verbose_name': '兼职信息',
                'db_table': 'yz_home_job',
            },
        ),
        migrations.AddField(
            model_name='applyjob',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homeapi.HomeJob', verbose_name='岗位'),
        ),
        migrations.AddField(
            model_name='applyjob',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
