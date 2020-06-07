from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Tag
import markdown
import re
from django.views.generic import ListView,DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.db.models import Q


class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        return super(IndexView,self).get_queryset().order_by('-created_time')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


class ArchiveView(IndexView):
    def get_queryset(self):
        return super(ArchiveView,self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                   created_time__month=self.kwargs.get('month')
                                   )


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)


class NavigationView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,name=self.kwargs.get('name'))
        return super(NavigationView,self).get_queryset().filter(tags=tag)


#  搜索
def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})