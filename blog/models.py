from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    contents = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение')
    published_at = models.DateTimeField(verbose_name='Дата публикации', auto_now=True)
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
