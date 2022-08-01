from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-pk',)
        abstract = True


class Seller(BaseModel):
    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def save(self, *args, **kwargs):
        if Customer.objects.filter(user=self.user).exists():
            raise ValidationError('Пользователь является покупателем')
        return super().save()


class Customer(BaseModel):
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def save(self, *args, **kwargs):
        if Seller.objects.filter(user=self.user).exists():
            raise ValidationError('Пользователь является продавцом')
        return super().save()


class Ad(models.Model):
    SHADES = (
        (
            'Green', (
                ('light-green', 'light-green'),
                ('dark-green', 'dark-green'),
            )
        ),
        (
            'Yellow', (
                ('light-yellow', 'light-yellow'),
                ('dark-yellow', 'dark-yellow'),
            )
        ),
    )
    flower = models.CharField(max_length=50, verbose_name='Вид цветка')
    shade = models.CharField(
        max_length=50, choices=SHADES,
        blank=True, verbose_name='Оттенок',
    )
    price = models.PositiveIntegerField(default=0, verbose_name='Цена', )
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество', )
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE,
        related_name='ads', verbose_name='Продавец'
    )
    visibility = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.flower

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'


class ManagerHidden(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(visibility=False)


class HiddenAds(Ad):
    objects = ManagerHidden()

    class Meta:
        proxy = True
        verbose_name = 'Скрытое объявление'
        verbose_name_plural = 'Скрытые объявления'


class Feedback(models.Model):
    title = models.CharField(max_length=50, blank=True, verbose_name='Тема отзыва', )
    text = models.TextField(verbose_name='Текст отзыва')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='feedbacks', verbose_name='Автор'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Purchase(models.Model):
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE,
        related_name='ads', verbose_name='Лот'
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='customers', verbose_name='Покупатель'
    )
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество', )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
