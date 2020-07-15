from django.shortcuts import render
# from api.models import userdetails,Product,wallet,order,hotel,storerestro,Doctor,Complain,Tax,cat,airport,airline,routes,days,book
from cab.models import carClass,cabdetails,cabOrder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
import random
# from .serializers import eventSerializer,UserSerializer,participateSerializer,EventSerializer,userDetailsSerializer
from rest_framework.generics import ListAPIView
# from .serializers import ProductSerializer,orderSerializer,userdetailsSerializer,UserSerializer,complainSerializer,transactionSerializer,catSerializer,hotelSerializer,hotelSerializer,airlineSerializer,routesSerializer,daysSerializer,airportSerializer
from .serializers import carClassSerializer,cabdetailsSerializer,cabOrderSerializer,kafkaSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import datetime
import time
from confluent_kafka import Producer, Consumer
import random
import json
import uuid




# import s2geometry as s2
def createmyuser(request):
    u = User.objects.create_superuser('ravi1','ravi2514999@myemail.com','maverick')
    u.save()
    return JsonResponse({'result':2})


def addcab(request):
    Username = request.GET.get('username')
    model = request.GET.get('carmodel')
    Registration = request.GET.get('carregistration')
    color = request.GET.get('carcolor')
    Type = int(request.GET.get('type'))

    

    typeArr = ['SEDAN','AUTO','BIKE','MINI']

    t = typeArr[Type]

    c = carClass.objects.get(cartype=t)
    user1 = User.objects.get(username=Username)
    ca = cabdetails(user=user1,cartype=c,carModel=model,carRegistration=Registration.upper(),carColor=color)
    ca.save()

    return JsonResponse({'result':1})


def caborder(request):
    Username = request.GET.get('username')
    latorigin = request.GET.get('latitudeorigin')
    longorigin = request.GET.get('longitudeorigin')
    latdestination = request.GET.get('latitudedestination')
    longdestination = request.GET.get('longitudedestination')
    Origin = request.GET.get('origin')
    Destination = request.GET.get('destination')
    Seat = request.GET.get('seat')
    Price = request.GET.get('price')
    Type = int(request.GET.get('type'))

    

    typeArr = ['SEDAN','AUTO','BIKE','MINI']

    t = typeArr[Type]

    c = carClass.objects.get(cartype=t)
    

    user1 = User.objects.get(username=Username)
    cid = 'CAB'+str(random.randint(9999,99999))    
    c = cabOrder(cartype=c,cabid=cid,user=user1,origin=Origin.upper(),destination=Destination.upper,latitudeOrigin=latorigin,longitudeOrigin=longorigin,latitudeDestination=latdestination,longitudeDestination=longdestination,seat=Seat,price=Price)

    c.save()

    return JsonResponse({'result':1})

def accept(request):
    cid = request.GET.get('cabid')
    Username = request.GET.get('username')
    
    c = cabdetails.objects.get(user__username=Username)
    co = cabOrder.objects.get(cabid=cid)
    co.cab = c
    co.accept=0
    co.save()



    return JsonResponse({'result':1})

def scanqr(request):
    cid = request.GET.get('cabid')
    
    co = cabOrder.objects.get(cabid=cid)
    co.accept=1
    co.save()
    serial = cabOrderSerializer(co)
    return JsonResponse({'details':serial.data})

def completeride(request):
    cid = request.GET.get('cabid')
    
    co = cabOrder.objects.get(cabid=cid)
    co.accept=2
    co.save()
    return JsonResponse({'result':1})

def showavailablerides(request):
    lat = request.GET.get('latitude')
    longi = request.GET.get('longitude')
    Username = request.GET.get('username')
    # S2 Library
    c = cabdetails.objects.get(user__username=Username)
    co = cabOrder.objects.filter(cab=None,cartype=c.cartype)
    list = []
    for c in co:
        serial = cabOrderSerializer(c)
        list.append({'User FirstName':serial.data['user']['first_name'],'cabid':serial.data['cabid'],'latitude':serial.data['latitudeOrigin'],'longitude':serial.data['longitudeOrigin']})

    return JsonResponse({'result':list})

def kafkaProduce(request):
    Username = request.GET.get('username')
    Latitude = request.GET.get('latitude')
    Longitude = request.GET.get('longitude')


    producer = Producer({
    'bootstrap.servers': 'pkc-l7pr2.ap-south-1.aws.confluent.cloud:9092',
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': '7AQPX7D57YCZZYFV',
    'sasl.password': '9De6dmWhaYomN26JULSABceMmAoeI6Ln5PCeQmTRYjv8SjXLwNczMVFplre3okw3'
    })

    data = {}
    data['id'] = str(random.randint(9999,99999))
    data['username'] = Username
    data['latitude'] = float(Latitude)
    data['longitude'] = float(Longitude)
    data['key'] = str(random.randint(9999,99999))
    
    message = json.dumps(data)
    future = producer.produce('cab',key=data['key'].encode('utf-8'),value=message.encode('utf-8'))

    producer.flush()

    return JsonResponse({'result':1})          


def consume(request):
    Username = request.GET.get('username')


    c = Consumer({
        'bootstrap.servers': 'pkc-l7pr2.ap-south-1.aws.confluent.cloud:9092',
        'sasl.mechanism': 'PLAIN',
        'security.protocol': 'SASL_SSL',
        'sasl.username': '7AQPX7D57YCZZYFV',
        'sasl.password': '9De6dmWhaYomN26JULSABceMmAoeI6Ln5PCeQmTRYjv8SjXLwNczMVFplre3okw3',
        'group.id': str(uuid.uuid1()),  
        'auto.offset.reset': 'earliest'
    })

    c.subscribe(['cab'])
    list = []


    def results(count):
        while count:
            msg = c.poll(0.1)
            
            if msg is None:
                continue
            if msg.error():
                continue
        
            m = msg.value().decode('ascii')
            
            z = json.loads(m)
            if z['username'] == Username:
                list.append(z)
                count -= 1
            

    results(1)
    return JsonResponse({'result':list})          
    # def events():
    #     try:
    #         while True:
    #             msg = c.poll(0.1)  # Wait for message or event/error
    #             if msg is None:
    #                 # No message available within timeout.
    #                 # Initial message consumption may take up to `session.timeout.ms` for
    #                 #   the group to rebalance and start consuming.
    #                 continue
    #             if msg.error():
    #                 # Errors are typically temporary, print error and continue.
    #                 print("Consumer error: {}".format(msg.error()))
    #                 continue
    #             m = msg.value()    
    #             yield msg.value()

    #         return Response({'result':events},mimetype)
            
        
    # except KeyboardInterrupt:
    #     pass

    # finally:
    #     # Leave group and commit final offsets
    #     c.close()

