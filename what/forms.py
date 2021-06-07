# -*- coding: utf-8 -*-

from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Recherche")
    instruments_qty = forms.IntegerField(required=True, label="Nombre d'instruments")
