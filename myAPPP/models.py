from django.db import models

# Create your models here. 创建了user表，4个字段


class User(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    # c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)  # 默认为False，也就是未进行邮件注册

    def __str__(self):
        return self.name

    class Meta:
        # ordering = ['-c_time']  # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)    # 哈希后的注册码
    user = models.OneToOneField('User')        # 1:1关系,一对一的形式
    cc_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ':  ' + self.code

    class Meta:
        ordering = ['-cc_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
