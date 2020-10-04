from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

# Create your views here.
from rest_framework import viewsets

from .serializers import HeroSerializer, SnippetSerializer,AssesmentItemSerislizer,AnswersSerializer
from .models import Hero, Snippet,AssesmentItem,Answers


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('id')
    serializer_class = HeroSerializer

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data), status = 200,content_type = "application/json")

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

def index(request):
    name = "mekonnen"
    return JsonResponse({'name':name,'age':23})

class AssesmentItemViewSet(viewsets.ModelViewSet):
    serializer_class = AssesmentItemSerislizer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = AssesmentItem.objects.filter(assesment_category=category)
        else:
            queryset = AssesmentItem.objects.all()
        return queryset

class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer