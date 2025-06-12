from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="agent_index"), # chama a view index
    path('api/chatbot/',views.chatbot_response, name='chatbot_response'), #chama a view chatbot_response
]