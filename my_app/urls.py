from django.urls import path
from .views import *

urlpatterns=[
    path('',article_list),
    path('article/<slug:slug>/',article_update),
    path('',ArticleList.as_view()),
    path('',ArticleDetails.as_view())
]