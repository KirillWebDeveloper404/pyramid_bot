from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import TildaArticle


def article(request):
    articles = TildaArticle.objects.all()
    article = articles[len(articles)-1]
    return render(request, 'tilda/article.html', {'article': article})
