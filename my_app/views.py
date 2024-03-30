from django.shortcuts import render,HttpResponse
from rest_framework import serializers
from . models import Article
from . serializers import ArticleSerializer
from django . http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework . views import APIView
from rest_framework . views import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404


# Create your views here.

@csrf_exempt
def article_list(request):
    if request.method=='GET':
        articles=Article.objects.all()
        serializers=ArticleSerializer(articles,many=True)
        return JsonResponse(serializers.data,safe=False)
    elif request.method=='POST':
        data=JSONParser().parse(request)
        serializers=ArticleSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data,status=201)
        return JsonResponse(serializers.errors,status=400)
    

@csrf_exempt
def article_update(request,slug):
    try:
        article=Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializers=ArticleSerializer(article)
        return JsonResponse(serializers.data)
    elif request.method == 'PUT': 
        data=JSONParser().parse(request)
        serializers = ArticleSerializer(article,data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data,status=200)
        return JsonResponse(serializers.errors,status=400)
    elif request.method == "DELETE": 
        article.delete()
        return HttpResponse(status=204)
    

class ArticleList(APIView):
    def get(self,request):
        article=Article.objects.all()
        serializers=ArticleSerializer(article,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers=ArticleSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    


class ArticleDetails(APIView):
    def get_object(self,slug):
        try:
            return Article.objects.get(slug=slug)    
        except Article.DoesNotExist:
            raise Http404
    def get(self,request,slug):
        article=self.get_object(slug)
        serializers=ArticleSerializer(article)
        return Response(serializers.data)
    def put(self,request,slug):
        article=self.get_object(slug)
        serializers=ArticleSerializer(article,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,slug):
        article=self.get_object(slug)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

