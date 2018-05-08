# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=70)  # 文章标题
    body = models.TextField()                # 文章正文
    created_time = models.DateTimeField()   #文章的创建时间
    modified_time = models.DateTimeField()  #最后一次修改时间
    views = models.PositiveIntegerField(default=0)  # 新增 views 字段记录阅读量

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    #分类与标签
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

        # 自定义 get_absolute_url 方法
        # 记得从 django.urls 中导入 reverse 函数

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])