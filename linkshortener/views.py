from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Link
from .forms import LinkShorterForm


def index(request):
    return HttpResponse("Hello, world from links!")


def create(request):
    template = loader.get_template('links/home.html')
    context = {'form': LinkShorterForm()}

    if request.method == 'GET':
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':

        used_form = LinkShorterForm(request.POST)

        if used_form.is_valid():
            user_link = request.POST['long_link']

            link = Link(long_link=user_link)
            link.save()

            context['new_link'] = request.build_absolute_uri('/') + link.short_link
            context['long_link'] = link.long_link

            return HttpResponse(template.render(context, request))

        return render(request, template, context)


def redirect(request, short_link):
    redirect_link = get_object_or_404(Link, short_link=short_link)

    redirect_link.followed_count += 1
    redirect_link.save()

    return HttpResponseRedirect(redirect_link.long_link)
