from random import randint

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from shortit.models import Urls
from url_shortner.settings import BASE_URL


@login_required
def shortit(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        url = request.POST.get("url", None),
        if url is not None:
            url = url[0]
            # Check if URL is valid
            test_url = URLValidator()
            try:
                test_url(url)
            except ValidationError:
                return render(request, "redirect.html")
            # Redirect to a success page.
            new_url = create_url(url)
            context = {'url': url,
                       'new_url': BASE_URL + new_url}
            # recording URL + Short
            new_record = Urls(destination=url,
                              short=BASE_URL + new_url)
            new_record.save()

            return render(request, "success.html", context)
        else:
            return render(request, "redirect.html")

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request, "redirect.html")

    return render(request, "redirect.html")


def create_url(url):
    allowed = "abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789-"
    new_name = ""
    for a in range(6):
        new_name = new_name + allowed[randint(0, len(allowed) - 1)]
    is_ever_used = Urls.objects.filter(short__iexact=new_name)
    if not is_ever_used:
        return new_name
    create_url(url)


@login_required
def actives(request):
    every_links = Urls.objects.all()
    context = {"Urls": every_links}
    return render(request, "list_active.html", context)


def redirect_view(request, url):
    if request.method == "GET":
        try:
            I_want_to_travel_to = Urls.objects.get(short__iexact=BASE_URL + url)
        except ObjectDoesNotExist:
            return redirect("/site/")

        if I_want_to_travel_to:
            context = {"url": I_want_to_travel_to.destination}
            return render(request, "redirection_page.html", context)
    return redirect("/site/")

@login_required
def flush_view(request):
    try:
        Urls.objects.all().delete()
    except ObjectDoesNotExist:
        pass
    return redirect("/")