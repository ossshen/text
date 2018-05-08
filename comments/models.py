# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.six import python_2_unicode_compatible

# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)                  #name（名字）
    email = models.EmailField(max_length=255)                #email
    url = models.URLField(blank=True)                        #url（个人网站）
    text = models.TextField()                                #内容
    created_time = models.DateTimeField(auto_now_add=True)   #时间

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]