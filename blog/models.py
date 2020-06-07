from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


# Create your models here.
# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 文章
class Post(models.Model):
    # 标题
    title = models.CharField('标题',max_length=70)
    # 作者
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    # 正文
    body = models.TextField('正文')
    # 创建时间和修改时间
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    # 阅读数
    views = models.PositiveIntegerField(default=0, editable=False)
    # 文章摘要
    excerpt = models.CharField('摘要',max_length=200,blank=True)
    # 标签
    tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    # 更新时间，生成摘要
    def save(self,*args,**kwargs):
        # 更新时间
        self.modified_time = timezone.now()
        # 生成摘要
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:100]
        super().save(*args,**kwargs)

    # 定义get_absolute_url方法
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk': self.pk})

    # 统计阅读量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title