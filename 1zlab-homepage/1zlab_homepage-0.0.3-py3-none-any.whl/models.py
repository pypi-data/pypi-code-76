from django.db import models


class HomePageThumbnail(models.Model):
    """主页项目展示表"""
    img_url = models.URLField(verbose_name="图片URL")
    title = models.CharField(max_length=31, verbose_name="标题")
    subtitle = models.CharField(max_length=63, verbose_name="副标题")
    introduction = models.TextField(max_length=511, verbose_name="介绍")
    content_url = models.URLField(verbose_name="内容链接")
    # 显示优先级, 越大越高
    rank = models.PositiveIntegerField(default=1, verbose_name="排序")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "homepage_thumbnail"
        verbose_name = "主页磁贴"
        verbose_name_plural = "主页磁贴"
