from django.db import models
from django.utils import timezone
from django.urls import reverse
from PIL import Image

class Hammock_variant(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name}'


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, blank=True, default='')
    inpost = models.CharField(max_length=100, blank=True, default='')
    comments = models.TextField(blank=True, default='')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    title = models.CharField(max_length=100)
    comment = models.TextField(blank=True, default='')
    date_created = models.DateTimeField(default=timezone.now)
    postal = models.BooleanField()
    image = models.ImageField(default='default.png', upload_to='orders_pics', blank=True)
    sumaric_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
    material = models.CharField(max_length=50, blank=True, default='')
    variants = models.ManyToManyField(Hammock_variant, through='Elements', blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    number_of_elements = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height >300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("orders-detail", kwargs={"pk": self.pk})   


class Elements(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(Hammock_variant, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    price_override = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)





