# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db.models import Count

from what.models import Composer


def search_composers(request):

    all_composers = []
    results = []

    if request.method == "POST":
        # Param for the request
        page = int(request.POST.get('page')) if int(request.POST.get('page')) > 0 else 1
        order = str(request.POST.get('order')) if str(request.POST.get('order')) else '-is_popular'

        # Request + filters
        all_composers = Composer.objects.annotate(works_count=Count('work')).order_by(order)
        # all_composers = all_composers.filter(death__year__lte=1900)
        # all_composers = all_composers.filter(name__contains="bach")

        # Pagination + final results
        page_composers = all_composers[((page-1)*30):(page*30)]
        for composer in page_composers:
            results.append({
                'id': composer.id,
                'name': composer.name,
                'first_name': composer.first_name,
                'portrait': composer.portrait,
                'works_count': composer.works_count,
            })

    data = {
        'total_count': len(all_composers),
        'page_count': len(results),
        'data': results
    }
    return JsonResponse(data)