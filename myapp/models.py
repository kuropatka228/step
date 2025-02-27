from django.db import models
from django.urls import reverse

class BaseShoe(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shoes/')

    class Meta:
        abstract = True

class Sneaker(BaseShoe):
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sneaker_detail', args=[str(self.id)])

class SneakerSize(models.Model):
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10)

class SneakerCollection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sneakers = models.ManyToManyField(Sneaker)

    def __str__(self):
        return self.title

class TopSneakerCategory(models.Model):
    name = models.CharField(max_length=255)
    sneakers = models.ManyToManyField(Sneaker, related_name='categories')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.sneaker.price