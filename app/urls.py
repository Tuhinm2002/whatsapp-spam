from django.urls import path
from . import views

urlpatterns=[path('',views.project,name="project"),path('add-text',views.text_add,name="text_add"),
path('add-img',views.image_add,name="image_add"),path('result/',views.result_func,name="result_func"),]


# ,path('result',views.result_func,name="result_func")