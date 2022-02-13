from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class MoveSectionEnum(models.IntegerChoices):
    PUBLISHEINPREPARECOMPETITION = 1, 'Prepared Competitions'
    ONLINEINCOMPETITION = 2, 'Ongoing Competitions'
    ARCHIVEDCOMPETITION = 3, 'Archived Competitions'


class GroupTitleEnum(models.IntegerChoices):
    FEATURECOMPETITION = 1, 'Featured Competition'
    ACTIVECOMPETITION = 2, 'Active Competition'


class Competition(models.Model):
    title = models.CharField(max_length=254,
                             verbose_name='Competition Title',
                             null=False,
                             blank=False)
    # image = models.ImageField()
    price = models.DecimalField(max_digits=20,
                                decimal_places=2,
                                null=False,
                                blank=False)
    letter_choices = models.CharField(max_length=3,
                                      help_text="Please enter range as A - Z",
                                      verbose_name="Ticket Letter Choices")
    number_from = models.CharField(max_length=7,
                                   help_text="Please enter range as 00 - 99",
                                   verbose_name="Ticket Number Choices",
                                   null=False,
                                   blank=False)
    total_tickets = models.PositiveIntegerField(null=False, blank=False)
    total_winners = models.PositiveIntegerField(default=1)
    actual_closing_date = models.DateTimeField(null=True, blank=True)
    ultimate_closing_date = models.DateTimeField(null=True, blank=True)
    description = RichTextField()
    group_title = models.SmallIntegerField(choices=GroupTitleEnum.choices)
    coupon_code_asked = models.BooleanField(default=False)
    move_section = models.SmallIntegerField(choices=MoveSectionEnum.choices)
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
    product_price = models.PositiveIntegerField(null=True,
                                                blank=True,
                                                verbose_name='Product Price')
    live_draw_link = models.URLField(max_length=10000,
                                     null=True,
                                     blank=True,
                                     default="https://google.com/")
    competition_date_reschedual = models.IntegerField(default=0, blank=True)
    total_earned = models.PositiveBigIntegerField(default=0, blank=True)

    @property
    def competition_image(self):
        return self.image.all().first()

    def __str__(self):
        return self.title


class CompetitionTicketStatusEnum(models.IntegerChoices):
    AVAILABLE = 1, "Available"
    SOLD = 2, 'Sold'
    RESERVED = 3, 'Reserved'


class CompetitionTicket(models.Model):
    competition = models.ForeignKey(Competition,
                                    on_delete=models.CASCADE,
                                    related_name='tickets')
    ticket = models.CharField(max_length=25)
    sold_time = models.DateTimeField(auto_now_add=False, null=True)
    status = models.SmallIntegerField(
        choices=CompetitionTicketStatusEnum.choices,
        default=CompetitionTicketStatusEnum.AVAILABLE)
    customer = models.ForeignKey(get_user_model(),
                                 on_delete=models.CASCADE,
                                 null=True)

    def __str__(self):
        id = str(self.ticket)
        return self.ticket


class CompetitionImage(models.Model):
    competition = models.ForeignKey(Competition,
                                    on_delete=models.CASCADE,
                                    related_name='images')
    image = models.ImageField(upload_to='competitions',
                              null=False,
                              blank=False)

    def __str__(self):
        return f'image:({str(id)})'