# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db.models import Count

from what.models import Composer


def search_composers(request):
    results = []
    if request.method == "POST":
        all_composers = Composer.objects.annotate(works_count=Count('work')).order_by('-is_popular', 'name')
        # all_composers = all_composers.filter(death__year__lte=1900)
        # all_composers = all_composers.filter(name__contains="bach")

        all_composers = all_composers[:30]
        for composer in all_composers:
            results.append({
                'id': composer.id,
                'name': composer.name,
                'first_name': composer.first_name,
                'portrait': composer.portrait,
                'works_count': composer.works_count,
            })

    data = {
        'count': len(results),
        'data': results
    }
    return JsonResponse(data)