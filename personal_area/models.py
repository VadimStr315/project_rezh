from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class AppealCategory(models.Model):  # Категория обращения (Жалоба, предложение...)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Constituency(models.Model):  # Избирательный округ
    id = models.IntegerField(db_index=True, primary_key=True)

    def __str__(self):
        return str(self.id)


class BenefitCategory(models.Model):  # Категория льгот автора обращения (пенсионер, инвалид...)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Decision(models.Model):  # Решение по обращению (Отказ, одобрено и.т.д.)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class ConsiderationStage(models.Model):  # Стадия обращения (Поступило, на рассмотрении, рассмотрено)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Deputy(models.Model):  # Депутат, тут еще скорее всего надо будет добавить поле фотографии
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    constituency = models.ForeignKey(Constituency, on_delete=models.PROTECT)

    def __str__(self):
        return '{0} {1} {2}'.format(self.surname, self.name, self.patronymic)

class Address(models.Model):  # Адресс автора обращения
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)  # Дом

    def __str__(self):
        return 'город {0}, улица {1}, дом {2}'.format(self.city, self.street, self.house)


class SocialStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Applicant(models.Model):  # Автор обращения
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT) # Address table
    benefit = models.ForeignKey(BenefitCategory, on_delete=models.PROTECT, null=True)
    social_status = models.ForeignKey(SocialStatus, on_delete=models.PROTECT)
    email = models.EmailField()
    phone = models.CharField(max_length=255)


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Appeal(models.Model):  # Обращение, тут тоже надо будет добавить поля для медиа-файлов.
    pin = models.IntegerField(null=True) # Поставить ограничение на null
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(AppealCategory, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    applicant = models.ForeignKey(Applicant, on_delete=models.PROTECT) # Applicant Table 
    content = models.TextField()
    decision = models.ForeignKey(Decision, on_delete=models.PROTECT)
    responsible_person = models.ForeignKey(Deputy, on_delete=models.PROTECT)
    consideration_stage = models.ForeignKey(ConsiderationStage, on_delete=models.PROTECT)
    decision_time = models.DateTimeField(null=True, default=None) # Должно устанавливаться по кнопке вынесения решения

    def get_absolute_url(self):
        return reverse('detail_appeal', kwargs={'appeal_id': self.pk})


class Sender(models.Model):
    sender = models.CharField(max_length=255)

    def __str__(self):
        return self.sender


class Message(models.Model):
    content = models.TextField()
    appeal = models.ForeignKey(Appeal, on_delete=models.PROTECT)
    deputy = models.ForeignKey(Deputy, on_delete=models.PROTECT)
    sender = models.ForeignKey(Sender, on_delete=models.PROTECT)
    applicant = models.ForeignKey(Applicant, on_delete=models.PROTECT)


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.ImageField(upload_to='photos/', null=True)
    cover = models.ImageField(upload_to='photos/', null=True)

    def __str__(self):
        return self.title