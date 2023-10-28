from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import json

from . import story_structure


def index(request):
    template = loader.get_template("singlepageapp/index.html")
    return HttpResponse(template.render({}, request))

def process_text(request):
    text = request.GET.get('text')
    '''
    images = []
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    images.append("https://th.bing.com/th/id/OIG.FHHLxc60Ib4KKZO7yefj?pid=ImgGn&w=1024&h=1024&rs=1'")
    '''
    prompts = story_structure.get_prompts_from_story_text(text)
    images = story_structure.get_images_from_prompts(prompts)
    return HttpResponse(json.dumps(images))