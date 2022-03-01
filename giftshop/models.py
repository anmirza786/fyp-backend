from distutils.command.upload import upload
from pydoc import describe
from unicodedata import name
from django.db import models
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField


# Create your models here.
class GiftShop(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    describe = RichTextField()
    discount_price = models.DecimalField(max_digits=20,
                                         decimal_places=2,
                                         null=True,
                                         blank=True,
                                         verbose_name='Discount Price',
                                         validators=[MinValueValidator(1)])
    discount_text = models.CharField(max_length=255, null=True, blank=True)
    discount_active = models.BooleanField(default=False,
                                          null=False,
                                          blank=False)
    product_price = models.DecimalField(max_digits=20,
                                        decimal_places=2,
                                        null=False,
                                        blank=False)
    image = models.ImageField(upload_to='giftshop/', blank=False, null=False)

    class Meta:
        ordering = ('-id', )

    def __str__(self):
        return str(self.title)

    # @property
    # def get_absolute_url(self):
    #     return f'/{self.slug}/'

    # def get_image(self):
    #     return
