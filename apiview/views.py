from django.shortcuts import render
from .serializers import ContainerSerializer
from .models import Container
from rest_framework import generics, permissions
from .tables import ContainerTable
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import ContainerFilter
from django.http import JsonResponse
import boto3
import json
from django.conf import settings
from datetime import datetime

class TodoCompletedList(generics.ListAPIView):
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #user = self.request.user
        return Container.objects.all()

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        #user = self.request.user
        return Container.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
        
        
        
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        #user = self.request.user
        return Container.objects.all()
    

class ContainerListView(SingleTableMixin, FilterView):
    model = Container
    table_class = ContainerTable
    template_name = 'home.html'
    filterset_class = ContainerFilter
    
    

def connect_to_aws(region,key,secret):
    sts = boto3.client('sts',
                  region_name=region, 
                  aws_access_key_id=key, 
                  aws_secret_access_key=secret)
    try:
        sts.get_caller_identity()
        return 1
    except Exception as e:
        print("Credentials are NOT valid.")
        return 0



def connect_to_kinesis(region,key,secret):
    client = boto3.client(
            "kinesis",
        region_name=region, 
        aws_access_key_id=key, 
        aws_secret_access_key=secret,
        )
    return client


def bucket_name(client,json_data):
    print('recieved')
    print(json_data)
    response = client.put_record(
            StreamName='Django-stream',
            Data= json.dumps(json_data),
            PartitionKey='customer_id'
        )
    print(json.dumps(json_data))
    print(response)
    
    
def helper(request):
    print('hi')
    print(request.POST['data'])
    json_data = {
        'data' :  request.POST['data'],
        'date_time' : str(datetime.now()),
        'customer_id' : request.user.username
    }
    print(json_data)
    print(settings.AWS_REGION, settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    validation = connect_to_aws(settings.AWS_REGION,settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    if validation:
        print('succesfully connected to AWS')
        kinesis_client = connect_to_kinesis(settings.AWS_REGION,settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket_name(kinesis_client,json_data)
    return JsonResponse({'Status':'Successfuly inserted'}, status = 200)