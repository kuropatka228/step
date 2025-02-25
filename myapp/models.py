from django.db import models
from django.urls import reverse

class BaseShoe(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shoes/')

    class Meta:
        abstract = True

class TopSneaker(BaseShoe):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    image = models.ImageField(upload_to='top_sneakers/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('top_sneaker_detail', args=[str(self.id)])

class Sneaker(BaseShoe):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='sneakers')

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

class Shoes(BaseShoe):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shoes/')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shoe_detail', args=[str(self.id)])


class TopSneakerCategory(models.Model):
    name = models.CharField(max_length=255)
    top_sneakers = models.ManyToManyField(TopSneaker)

    def __str__(self):
        return self.name