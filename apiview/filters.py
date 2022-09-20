import django_filters
from .models import *

class ContainerFilter(django_filters.FilterSet):
    class Meta:
        model = Container
        fields = ['stock_name']
