from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee', verbose_name='Пользователь')
    phone = models.CharField(max_length=50, verbose_name='Телефон')


class Food(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(verbose_name='Фотография')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PREPARING = 'preparing'
    STATUS_ON_WAY = 'on_way'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_PREPARING, 'Готовится'),
        (STATUS_ON_WAY, 'В пути'),
        (STATUS_DELIVERED, 'Доставлен'),
        (STATUS_CANCELED, 'Отменён')
    )

    contact_phone = models.CharField(max_length=50, verbose_name='Контактный телефон')
    contact_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    delivery_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Адрес доставки')


class OrderFoods(models.Model):
    order = models.ForeignKey(Order, related_name='foods', verbose_name='Заказ', on_delete=models.PROTECT)
    food = models.ForeignKey(Food, related_name='+', verbose_name='Блюдо', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Количество')


# order.foods.first().food.name
# order.foods.first().amount