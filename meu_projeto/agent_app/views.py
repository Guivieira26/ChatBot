from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from crewai import LLM, Agent, Task, Crew, Process
from textwrap import dedent
import os
from dotenv import load_dotenv
# Create your views here.
#AI configurations
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = LLM(
    model="azure/gpt-4.1-nano",
    api_key=api_key,
    api_base="https://marin-m7gr5ypk-eastus2.openai.azure.com/",
    api_version="2025-01-01-preview",
    temperature=0.3,
    max_tokens=500
)

planner = Agent(
    role="Chat isbot",
    goal="responder de maneira ignorante e com raiva todas as perguntas do usuário.",
    backstory=dedent("Pode falar o que quiser."),
    verbose=True,
    llm=llm
)

def gerar_resposta_usuario(pergunta_do_usuario):
    """Função que transforma a pergunta do usuário em uma resposta via agente CrewAI."""
    plan_task = Task(
        description=f"Responda de forma ignorante como se estivesse com raiva a seguinte pergunta do usuário: {pergunta_do_usuario}",
        #description=f"Responda de forma ignorante e burra a seguinte pergunta do usuário: {pergunta_do_usuario}",
        expected_output="Uma resposta ignorante e intimidadora para o usuário.",
        agent=planner,
        async_execution=False
    )

    crew = Crew(
        agents=[planner],
        tasks=[plan_task],
        process=Process.sequential,
        verbose=False
    )

    resultado = crew.kickoff()
    return resultado
#def index(request):
#    return HttpResponse("agent app teste")  # Teste
def index(request):
    return render(request, 'agent_app/agent.html')

@csrf_exempt  # Desativa a proteção CSRF para esta view, se necessário
def chatbot_response(request):
    #return HttpResponse("Hello agent aqui tem chat")  # Teste
    #print("Recebendo requisição para chatbot_response", flush=True)
    if request.method == 'POST':
        #print("Recebendo mensagem do usuário", flush=True)
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Aqui você pode adicionar a lógica para processar a mensagem do usuário
        # Por exemplo, responder com uma mensagem fixa ou integrar com um modelo de IA
        response_message = gerar_resposta_usuario(user_message)
        #print("Resposta gerada pelo agente:", response_message, flush=True)

        return JsonResponse({'response': str(response_message)})

    return JsonResponse({'error': 'Método não permitido'}, status=405)  # Método não permitido