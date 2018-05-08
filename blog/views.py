# -*- coding: utf-8 -*-
import markdown


from comments.forms import CommentForm
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from comments.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 2) # 每页显示 2 个联系人

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html',context={'contacts': contacts})


def detail(request, pk):       #文章详情页面
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    post.increase_views()
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):               #归档
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    paginator = Paginator(post_list, 2)  # 每页显示 2 个联系人

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html',context={'contacts': contacts})


def category(request, pk):                        #分类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    paginator = Paginator(post_list, 2)  # 每页显示 2 个联系人

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html',context={'contacts': contacts})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(Tag=tag).order_by('-created_time')
    paginator = Paginator(post_list, 2)  # 每页显示 2 个联系人

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html',context={'contacts': contacts})


def  contact(request):
    return render(request, 'blog/contact.html')


def  about(request):
    return render(request, 'blog/about.html')



