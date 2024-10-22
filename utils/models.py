from datetime import time

from django.db import models


class Base(models.Model):
    """
    Base modelo criada para já conter o campos created_at e updated_at que estão presentes em todas as tabelas.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Schedules(models.TextChoices):
    HOUR_06_00 = (time(6, 0), '06:00')
    HOUR_06_30 = (time(6, 30), '06:30')
    HOUR_07_00 = (time(7, 0), '07:00')
    HOUR_07_30 = (time(7, 30), '07:30')
    HOUR_08_00 = (time(8, 0), '08:00')
    HOUR_08_30 = (time(8, 30), '08:30')
    HOUR_09_00 = (time(9, 0), '09:00')
    HOUR_09_30 = (time(9, 30), '09:30')
    HOUR_10_00 = (time(10, 0), '10:00')
    HOUR_10_30 = (time(10, 30), '10:30')
    HOUR_11_00 = (time(11, 0), '11:00')
    HOUR_11_30 = (time(11, 30), '11:30')
    HOUR_12_00 = (time(12, 0), '12:00')
    HOUR_12_30 = (time(12, 30), '12:30')
    HOUR_13_00 = (time(13, 0), '13:00')
    HOUR_13_30 = (time(13, 30), '13:30')
    HOUR_14_00 = (time(14, 0), '14:00')
    HOUR_14_30 = (time(14, 30), '14:30')
    HOUR_15_00 = (time(15, 0), '15:00')
    HOUR_15_30 = (time(15, 30), '15:30')
    HOUR_16_00 = (time(16, 0), '16:00')
    HOUR_16_30 = (time(16, 30), '16:30')
    HOUR_17_00 = (time(17, 0), '17:00')
    HOUR_17_30 = (time(17, 30), '17:30')
    HOUR_18_00 = (time(18, 0), '18:00')
    HOUR_18_30 = (time(18, 30), '18:30')
    HOUR_19_00 = (time(19, 0), '19:00')
    HOUR_19_30 = (time(19, 30), '19:30')
    HOUR_20_00 = (time(20, 0), '20:00')
    HOUR_20_30 = (time(20, 30), '20:30')
    HOUR_21_00 = (time(21, 0), '21:00')
    HOUR_21_30 = (time(21, 30), '21:30')
    # HOUR_22_00 = (time(22, 0), '22:00') Não pode conter este horário pois é quando fecha
    