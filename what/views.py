import json, urllib, datetime, re, itertools

from django.http import HttpResponse
from django.shortcuts import render

from django.db.models import Count

# Create your views here.
from what.models import Composer, Work, Instrument, WorkVersion, WorkVersionEnsemble

from what.forms import SearchForm


def index(request):
    return render(request, "what-index.html")







# Pour vérifier les ids qui sont valides pour les oeuvres chez OpenOpus
def check(request, start, end):
    wrong_ids = []
    for oo_id in range(start, end):
        # Fetch the composers for the letter
        url = "https://api.openopus.org/work/detail/%s.json" % oo_id
        data = urllib.request.urlopen(url).read().decode()
        obj = json.loads(data)
        if oo_id % 50 == 0:
            print(oo_id)
        if obj['status']['success'] == 'false':
            wrong_ids.append(oo_id)
    print(wrong_ids)
    print(len(wrong_ids))
    return HttpResponse("Nombre d'ids absents : " + str(len(wrong_ids)))




""" IMPORTANT """

# from collections.abc import Iterable
#
# def flatten(l):
#     for el in l:
#         if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
#             yield from flatten(el)
#         else:
#             yield el


def get_instruments_categories(cat_id=0):
    sub_cats = Instrument.objects.filter(parent_id=cat_id).order_by('sequence')
    return {
        'id': cat_id,
        'name': Instrument.objects.get(id=cat_id).name,
        'categories': [get_instruments_categories(subcat.id) for subcat in sub_cats] if sub_cats else None,
    }

def get_instrument_categories_names(category, prefix="", all_cats=[]):
    if prefix=="":
        all_cats = []
    all_cats.append({'id': int(category["id"]), 'name': prefix + category["name"]})
    if category["categories"]:
        for sub_cat in category["categories"]:
            get_instrument_categories_names(sub_cat, prefix + category["name"]+"/", all_cats)
    return all_cats




""" AUTRE """

def create_mass_work_version(request):

    searched_works = []
    already_saved_works = []
    instruments_qty = ''

    if request.method == "POST":
        # If we made a search
        if request.POST.get("search"):
            # all searched works
            searched_works = Work.objects.filter(name__icontains=request.POST.get("search"))
            # works versions existing for the work fetched
            already_saved_versions = WorkVersion.objects.filter(work_id__in=searched_works)
            # already saved works
            already_saved_works = Work.objects.filter(id__in=[w.work_id.id for w in already_saved_versions])

            for i in range(1, int(request.POST.get("instruments_qty"))+1 ):
                instruments_qty += str(i)


        # If we actually want to create work version
        if request.POST.get("send"):
            selected_works = []
            selected_instruments = {}
            for var in request.POST:
                if var[:7] == "work_id":
                    selected_works.append(int(var.replace("work_id_", "")))
                elif var[:11] == "instrument_":
                    instrument_id = int(request.POST.get(var))
                    if instrument_id not in selected_instruments:
                        selected_instruments[instrument_id] = 0
                    selected_instruments[instrument_id] += 1

            print("========================================")
            for work in selected_works:
                w = Work.objects.get(id=work)
                print("Save... "+w.name)
                wv = WorkVersion(work_id=w, is_original=True)
                wv.save()
                for i_id in selected_instruments:
                    wv.instruments_ids.add(i_id, through_defaults={'quantity': selected_instruments[i_id]})
                wv.save()

            print("========================================")



    print(already_saved_works)
    all_instruments = get_instruments_categories()
    all_instruments_names = get_instrument_categories_names(all_instruments)

    form = SearchForm()

    return render(
        request,
        "what-create-mass-work-version.html",
        {
            'form': form,
            'works': searched_works,
            'works_qty': len(searched_works),
            'saved_works': already_saved_works,
            'instruments': all_instruments_names,
            'instruments_qty': instruments_qty,
        }
    )







"""
    ********************************************
    ***              BROWSE                  ***
    ********************************************
"""


def browse(request):
    return render(request, "what-browse.html")


# Browse composers  ('/what/composers/')
def browse_composers(request):
    all_composers = Composer.objects.annotate(works_qty=Count('work')).order_by('-is_popular')
    # print(all_composers)
    return render(request, "what-composers.html")


# Browse  works     ('/what/works/')
def browse_works(request):
    return render(request, "what-browse-works.html")


# Display a specific composer's details  ('/what/composers/@ID-name-slugged')
def browse_composer_details(request, composer_id):
    return render(request, "what-browse-composer-details.html", context={'composer_id': composer_id})


# Display a specific work's details  ('/what/works/@ID-name-slugged')
def browse_work_details(request, work_id):
    return render(request, "what-browse-work-details.html", context={'work_id': work_id})



"""
    ********************************************
    ***              SEARCH                  ***
    ********************************************
"""


def search(request):
    return render(request, "what-search.html")
