from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date 
# Create your views here.
import json   
# @api_view(['GET'])      
# def github(request):
    # mydate=date
    # print(mydate)
#     date="2021-07-18"
#     tasks = requests.get(f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc")
#     my_data= tasks.json()
#     return Response(my_data["items"])   
          
          
def github(request):
    date="2021-07-18"       
    tasks = requests.get(f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc")
    data= tasks.json()
    language=data["items"]     
    for i in language:
        length=filter(lambda x: x["language"] ==i["language"],language)
        num=len(list(length))
        # print(num)
    context={"language":language,"num":num}    
    return render(request,"api.html",context)  
   
   
