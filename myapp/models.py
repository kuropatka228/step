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

class Shoes(BaseShoe):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shoes/')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shoe_detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.text}'

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return f'Order {self.id} - {self.customer_name}'


class TopSneakerCategory(models.Model):
    name = models.CharField(max_length=255)
    top_sneakers = models.ManyToManyField(TopSneaker)

    def __str__(self):
        return self.name