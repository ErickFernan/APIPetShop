import django_filters

from datetime import datetime, time


class DateToEndOfDayFilter(django_filters.DateFilter):
    """Filtro que ajusta a data para o final do dia (23:59:59.999999)"""
    def filter(self, qs, value):
        if value:
            value = datetime.combine(value, time(23, 59, 59, 999999))
            return super().filter(qs, value)
        return qs


# NÃO FAZ SENTIDO USAR ESSA CLASSE, POIS O DJANGO CONVERTE AUTOMÁTICAMENTE O DATEFILTER NO TIPO datetime(ANO, MÊS, DIA, 0, 0, 0)
# class DateToStartOfDayFilter(django_filters.DateFilter):
#     """Filtro que ajusta a data para o início do dia (00:00:00)"""
#     def filter(self, qs, value):
#         if value:
#             value = datetime.combine(value, time.min)  # 00:00:00
#             return super().filter(qs, value)
#         return qs
