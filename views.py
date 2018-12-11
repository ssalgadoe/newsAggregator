from django.shortcuts import render, get_object_or_404
from .models import  active_news_items
import random


# Create your views here.




def index(request):
    news_list = sorted(active_news_items.objects.all().values().order_by('?'), key=lambda x:random.random())
    last_update = news_list[0]['time_st']
    is_mobile =request.user_agent.is_mobile

    context = {
        'news_list': news_list,
        'last_update': last_update,
        'is_mobile': is_mobile,

    }
    return render(request, 'news/index.html',context)


def news_data(request,news_id):
    is_mobile = request.user_agent.is_mobile
    try:
        news_dt = active_news_items.objects.values("title", "body", "source", "time_st").distinct().filter(id=news_id)
    except news_items.DoesNotExist:
        raise Http404("News Doesn't exist")
    context = {'news_data': news_dt,
               'is_mobile': is_mobile,
               }
    return render(request, 'news/news_data.html', context)
