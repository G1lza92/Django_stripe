from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html_join

from users.models import User

CURRENCY = (
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
        ('GBP', 'Great Britain Pound'),
    )


class Item(models.Model):
    """ Item model """
    name = models.CharField(
        'Item name',
        max_length=255,
        unique=True,
    )
    description = models.TextField()
    price = models.FloatField(
        'Item price',
        validators=[MinValueValidator(0.01, 'Price cannot be 0 or negative')],
    )
    # currency = models.CharField( # Новое поле, миграций нет
    #     'Item currency',
    #     max_length=3,
    #     default='USD',
    #     choices=CURRENCY,
    # )
    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Order model """
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField(
        Item,
        through='ItemsInOrder'
    )
    total_price = models.FloatField(
        'Total_cost',
        null=True,
        blank=True,
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status',
    )
    stripe_session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_cost(self):
        items_in_order = ItemsInOrder.objects.filter(order=self)
        return sum(item_in_order.item.price * item_in_order.quantity for item_in_order in items_in_order)

    def get_items(self):
        items_in_order = ItemsInOrder.objects.filter(order=self)
        return format_html_join(
            '\n',
            '<li>{} (quantity: {})</li>',
            ((item_in_order.item.name, item_in_order.quantity) for item_in_order in items_in_order),
        )
    get_items.short_description = 'Items'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_on']


class ItemsInOrder(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Quantity cannot be less than 1')],
    )
