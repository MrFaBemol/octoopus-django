# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db.models import Count, F

from what.models import Composer


def search_composers(request):

    all_composers = []
    results = []

    if request.method == "POST":
        # Param for the request
        page = int(request.POST.get('page')) if int(request.POST.get('page')) > 0 else 1

        name = str(request.POST.get('name')) if request.POST.get('name') else ''

        if request.POST.get('order_by') and str(request.POST.get('order_by')) == 'default':
            order_by = 'is_popular'
            ordering = 'descending'
        else:
            order_by = str(request.POST.get('order_by')) if request.POST.get('order_by') else 'name'
            ordering = str(request.POST.get('ordering')) if request.POST.get('ordering') else 'ascending'

        # Request + filters
        all_composers = Composer.objects.annotate(works_quantity=Count('work'))
        all_composers = all_composers.filter(name__contains=name) | all_composers.filter(first_name__contains=name)

        # Ordering
        if ordering == 'ascending':
            all_composers = all_composers.order_by(F(order_by).asc(nulls_last=True))
        else:
            all_composers = all_composers.order_by(F(order_by).desc(nulls_last=True))

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
                'works_quantity': composer.works_quantity,
            })

    data = {
        'total_count': len(all_composers),
        'page_count': len(results),
        'data': results
    }
    return JsonResponse(data)