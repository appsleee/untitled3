from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)


# 创建超级管理员,用户名为：admin ，密码为：admin666

#  2018-1-16 21:31:16

admin.site.register(models.ConfirmString)