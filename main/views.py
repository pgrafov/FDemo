import re
from random import randint

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from main.forms import UrlForm
from main.models import Url, Word


def user_link(request, path):
    try:
        word = Word.objects.get(title=path)
        url = Url.objects.get(word=word)
        return HttpResponseRedirect(url.link)
    except (Word.DoesNotExist, Url.DoesNotExist):
        return render(request, '404.html', status=404)


def home(request):
    last_link = None
    invalid_link = False
    if request.method == 'POST':
        urlform = UrlForm(request.POST)
        if urlform.is_valid():
            link = urlform.cleaned_data['link']
            if Url.objects.filter(link=link).count() > 0:
                existing_url = Url.objects.get(link=link)
                existing_short_link = request.build_absolute_uri(existing_url.word.title) + '/'
                return render(request, 'index.html', {'urlform': UrlForm(),
                                                      'last_link': existing_short_link})
            all_words = Word.objects.all()
            unassigned_words = Word.objects.filter(assigned=False)
            if all_words.count() == 0:
                return HttpResponse("Server fault: empty database", status=500)
            if unassigned_words.count() > 0:
                # pick the first word in the wordlist that is a part of URL
                url_words = re.split('[^0-9a-z]*', link.lower())
                url_words = [w for w in url_words if len(w) > 0]
                matching_words = Word.objects.filter(title__in=url_words,
                                                     assigned=False).order_by('title')
                if matching_words.count() != 0:
                    word = matching_words[0]
                else:
                    # then choose a random one
                    random_idx = randint(0, unassigned_words.count() - 1)
                    word = Word.objects.filter(assigned=False)[random_idx]
            else:
                oldest_url = Url.objects.order_by('created')[0:1].get()
                word = oldest_url.word
                oldest_url.delete()
            word.assigned = True
            word.save()
            url = Url(link=link, word=word)
            last_link = request.build_absolute_uri(word.title) + '/'
            url.save()
        else:
            if 'link' in urlform.data:
                invalid_link = urlform.data['link']
    return render(request, 'index.html', {'urlform': UrlForm(),
                                          'invalid_link': invalid_link,
                                          'last_link': last_link})
