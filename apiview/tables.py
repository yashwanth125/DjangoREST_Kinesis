import django_tables2 as tables
from .models import Container

class ContainerTable(tables.Table):
    class Meta:
        model = Container
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("stock_name", "stock_price" )