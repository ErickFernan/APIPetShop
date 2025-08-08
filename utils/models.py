from datetime import time

from django.db import models


class BaseModel(models.Model):
    """
    Base modelo criada para já conter o campos created_at e updated_at que estão presentes em todas as tabelas.
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

class Schedules(models.TextChoices):
    HOUR_06_00 = '06:00'
    HOUR_06_30 = '06:30'
    HOUR_07_00 = '07:00'
    HOUR_07_30 = '07:30'
    HOUR_08_00 = '08:00'
    HOUR_08_30 = '08:30'
    HOUR_09_00 = '09:00'
    HOUR_09_30 = '09:30'
    HOUR_10_00 = '10:00'
    HOUR_10_30 = '10:30'
    HOUR_11_00 = '11:00'
    HOUR_11_30 = '11:30'
    HOUR_12_00 = '12:00'
    HOUR_12_30 = '12:30'
    HOUR_13_00 = '13:00'
    HOUR_13_30 = '13:30'
    HOUR_14_00 = '14:00'
    HOUR_14_30 = '14:30'
    HOUR_15_00 = '15:00'
    HOUR_15_30 = '15:30'
    HOUR_16_00 = '16:00'
    HOUR_16_30 = '16:30'
    HOUR_17_00 = '17:00'
    HOUR_17_30 = '17:30'
    HOUR_18_00 = '18:00'
    HOUR_18_30 = '18:30'
    HOUR_19_00 = '19:00'
    HOUR_19_30 = '19:30'
    HOUR_20_00 = '20:00'
    HOUR_20_30 = '20:30'
    HOUR_21_00 = '21:00'
    HOUR_21_30 = '21:30'
    # HOUR_22_00 = '22:00', '22:00'  # Removido, pois é o horário de fechamento
    