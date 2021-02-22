from django.shortcuts import render

from homepage.models import HomePageThumbnail


def index(request):
    homepagethumbnail_list = HomePageThumbnail.objects.all().order_by('-rank')
    context = {'homepagethumbnail_list': homepagethumbnail_list}
    return render(request, 'homepage/index.html', context)
