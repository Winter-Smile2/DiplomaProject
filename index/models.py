from django.db import models

# Create your models here.

class LinkSpider(models.Model):
    link_id = models.IntegerField('序号',primary_key=True)
    link_name = models.CharField('链接地址',max_length=50)
    image = models.ImageField('图片',upload_to='../media/index_images')
    title = models.CharField('文章标题',max_length=55)
    class Meta:
        db_table = 'index_link'

