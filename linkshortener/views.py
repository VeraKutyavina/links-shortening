from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .forms import LinkShorterForm
from .models import Link


# view for redirect on create page
def index(request):
    return HttpResponseRedirect(reverse('create'))


# view for create link
def create(request):
    template = loader.get_template('links/home.html')
    context = {'form': LinkShorterForm()}

    # return template with form on GET query
    if request.method == 'GET':
        return HttpResponse(template.render(context, request))

    # return info about new url on POST query
    elif request.method == 'POST':

        used_form = LinkShorterForm(request.POST)

        print(request.POST)

        if used_form.is_valid():
            user_link = request.POST['long_link']

            print(user_link)

            link = Link(long_link=user_link)
            link.save()

            context['new_link'] = request.build_absolute_uri('/') + link.short_link
            context['long_link'] = link.long_link

            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))


# view for redirect on origin url form encoded
def redirect(request, short_link):
    redirect_link = get_object_or_404(Link, short_link=short_link)
    redirect_link.followed_count += 1
    redirect_link.save()

    return HttpResponseRedirect(redirect_link.long_link)


# view for get links list
def all_links(request):
    links = Link.objects.order_by("-followed_count")
    template = loader.get_template('links/allLinks.html')
    content = template.render({"links": links, "absolute_url": request.build_absolute_uri('/')}, request)

    return HttpResponse(content=content)


# view for remove link
def remove(request, link_id):
    removed_link = Link.objects.get(pk=link_id)
    removed_link.delete()

    return HttpResponseRedirect(reverse('allLinks'))
