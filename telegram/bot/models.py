from django.db import models
from datetime import datetime
import decimal


def image_folder(instance, filename):
    filename = str(instance.id) + '.' + filename.split('.')[1]
    return "transactions/{0}/{1}/{2}".format(instance.type, instance.broker.user_id, filename)


class Profile(models.Model):
    invited_by = models.ForeignKey('Profile', to_field='user_id', on_delete=models.SET_NULL, blank=True, null=True)
    user_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=450, null=True, blank=True)
    last_name = models.CharField(max_length=450, null=True, blank=True)
    username = models.CharField(max_length=450, null=True, blank=True)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    created_on = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Transaction(models.Model):
    broker = models.ForeignKey('Profile', to_field='user_id', on_delete=models.PROTECT)
    card = models.CharField(max_length=200, blank=True, null=True)
    TRANSACTION_TYPE = [
        ('V', 'Вывод'),
        ('P', 'Пополнение'),
    ]
    type = models.CharField(max_length=1, choices=TRANSACTION_TYPE)
    verified = models.BooleanField(default=False)
    sum = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to=image_folder, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sum)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-pub_date']


class VerifiedTransaction(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.PROTECT)
    verified_sum = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'VerifiedTransaction'
        verbose_name_plural = 'VerifiedTransactions'
        ordering = ['-pub_date']

    def save(self, *args, **kwargs):
        t = Profile.objects.get(user_id=self.transaction.broker.user_id)
        if self.transaction.type == 'P':
            t.balance = decimal.Decimal(self.verified_sum * decimal.Decimal(0.90) + t.balance).quantize(
                decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
            if t.invited_by:
                who_invited = Profile.objects.get(user_id=t.invited_by.user_id)
                who_invited.balance = decimal.Decimal(
                    self.verified_sum * decimal.Decimal(0.05) + who_invited.balance).quantize(
                    decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
                who_invited.save()
        elif self.transaction.type == 'V':
            t.balance = t.balance - self.verified_sum
        t.save()
        transaction = Transaction.objects.get(id=self.transaction.id)
        transaction.verified = True
        transaction.save()
        super().save(*args, **kwargs)
