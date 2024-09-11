from django.core.validators import RegexValidator
from django.db import models


class BlogPost(models.Model):

    title = models.CharField(max_length=32, verbose_name="заголовок")
    image = models.ImageField(upload_to="media/")
    content = models.TextField(verbose_name="содержимое статьи")
    created_at = models.DateField(verbose_name="дата создания статьи", auto_now_add=True)
    viewed = models.IntegerField(default=0, verbose_name="количество просмотров")

    def __str__(self):
        return f"{self.title} {self.created_at}"

    class Meta:
        verbose_name = 'Запись в блоге'
        verbose_name_plural = "записи в блоге"
        ordering = ('title', 'created_at',)
