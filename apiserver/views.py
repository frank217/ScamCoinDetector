from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

import json
import os

from repos.models import Coin
from .settings import APP_DIR


def main(request):
    context = dict()

    # references to client-side templates and sprite sheets
    context['tags'] = os.listdir(os.path.join(APP_DIR, 'static', 'tags'))
    context['sprite_sheets'] = os.listdir(os.path.join(APP_DIR, 'static', 'thumb_sprites'))

    # preload data to skip initial ajax calls
    with open(os.path.join(APP_DIR, 'templates', 'sprites.json')) as f:
        context['sprites'] = f.read()

    context['movies'] = json.dumps([_overview(m) for m in Coin.objects.all()])

    return render(request, "index.html", context=context)


def _overview(coin):
    return {
        'id': int(coin.coin_id),
        'name': coin.coin_name,
        'github_link': coin.github_link,
        'readme_score': coin.readme_score,
        'num_contributors': coin.active_contributors,
        'issues_score': coin.issues_score,
        'pr_score': coin.pr_score
    }


def _details(coin):
    return {
    }


def api_details(request, rt_id):
    try:
        m = Coin.objects.get(rt_id=rt_id)
    except ObjectDoesNotExist:
        r = JsonResponse({
            'error': "Movie with id '{}' was not found.".format(rt_id)
        })
        r.status_code = 404
        return r

    return JsonResponse(_details(m))
