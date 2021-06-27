# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db.models import Count, F, Case, When, Value, IntegerField

from what.models import Composer, Instrument
from api.shared.tools import get_instrument_parent_category
from Octoopus.shared.tools import load_config


def search_composers(request):

    data = {}

    if request.method == "POST":
        all_composers = []

        # Param for the request
        request_id = int(request.POST.get('request_id')) if request.POST.get('request_id') else 0
        page = int(request.POST.get('page')) if int(request.POST.get('page')) > 0 else 1
        name = str(request.POST.get('name')) if request.POST.get('name') else ''

        if request.POST.get('order_by') and str(request.POST.get('order_by')) == 'default':
            order_by = 'is_popular'
            ordering = 'descending'
        else:
            order_by = str(request.POST.get('order_by')) if request.POST.get('order_by') else 'name'
            ordering = 'descending' if request.POST.get('ordering') == 'on' else 'ascending'

        # Null safety for dates
        dates = {}
        for date in ['min_birth','max_birth','min_death', 'max_death']:
            try:
                dates[date] = int(request.POST.get(date))
            except:
                dates[date] = -1


        # Request
        all_composers = Composer.objects.annotate(works_quantity=Count('work'))


        # ######################### Filters #########################
        # Name
        all_composers = all_composers.filter(name__contains=name) | all_composers.filter(first_name__contains=name)

        # Popular / Essential options
        if request.POST.get('is_popular') and request.POST.get('is_popular') == 'on':
            all_composers = all_composers.filter(is_popular=True)
        if request.POST.get('is_essential') and request.POST.get('is_essential') == 'on':
            all_composers = all_composers.filter(is_essential=True)

        # Dates
        if dates['min_birth'] != -1:
            all_composers = all_composers.filter(birth__year__gte=dates['min_birth'])
        if dates['max_birth'] != -1:
            all_composers = all_composers.filter(birth__year__lte=dates['max_birth'])
        if dates['min_death'] != -1:
            all_composers = all_composers.filter(death__year__gte=dates['min_death'], death__isnull=False)
        if dates['max_death'] != -1:
            all_composers = all_composers.filter(death__year__lte=dates['max_death'], death__isnull=False)

        # ######################### Ordering ########################
        if ordering == 'ascending':
            all_composers = all_composers.order_by(F(order_by).asc(nulls_last=True))
        else:
            all_composers = all_composers.order_by(F(order_by).desc(nulls_last=True))

        # Patches
        if order_by == 'death':
            all_composers = all_composers.filter(death__isnull=False)


        # Pagination & final results ########################
        config = load_config('what')
        res_per_page = int(config['composers']['results_per_page'])
        page_composers = all_composers[((page-1)*res_per_page):(page*res_per_page)]

        page_results = []

        for composer in page_composers:
            page_results.append({
                'id': composer.id,
                'name': composer.name,
                'first_name': composer.first_name,
                'slug': composer.slug,
                'portrait': composer.portrait,
                'works_quantity': composer.works_quantity,
            })

        data = {
            'request_id': request_id,
            'page': page,
            'total_count': len(all_composers),
            'page_count': len(page_results),
            'composers': page_results,
            'results_per_page': res_per_page
        }


    return JsonResponse(data)


def search_instruments(request):

    data = {}

    if request.method == "POST":
        # Param for the request
        request_id = int(request.POST.get('request_id')) if request.POST.get('request_id') else 0
        search = str(request.POST.get('search')) if request.POST.get('search') else ''


        all_instruments = Instrument.objects.all()
        search_terms = [term for term in search.split(' ') if term != ""]

        # Todo: ajouter un exact_results

        best_results = all_instruments.filter(name__contains=search_terms[0])
        for i in range(1, len(search_terms)):
            best_results = best_results & all_instruments.filter(name__contains=search_terms[i])

        print(best_results)

        all_results = best_results

        # all_results = (
        #     Instrument.objects
        #     .filter(best_results | all_instruments)
        #     .annotate(
        #         search_ordering=Case(
        #             When(best_results, then=Value(2)),
        #             When(all_instruments, then=Value(1)),
        #             default=Value(-1),
        #             output_field=IntegerField(),
        #         )
        #     ).order_by('-search_ordering', ...)
        # )

        print(all_results)

        # ORDER & LIMIT
        all_results = all_results[:5]

        propositions = []
        for instrument in all_results:
            propositions.append({
                'id': instrument.id,
                'name': instrument.name,
                'full_path': get_instrument_parent_category(instrument.id),
            })

        data = {
            'request_id': request_id,
            'search_terms': search_terms,
            'total_count': len(propositions),
            'propositions': propositions,
        }

    return JsonResponse(data)