# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify


"""
    ********************************************
    ***               Misc                   ***
    ********************************************
"""


class Period(models.Model):
    name = models.CharField(max_length=60)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=3, default="")
    flag_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name




"""
    ********************************************
    ***             Composers                ***
    ********************************************
"""


class Composer(models.Model):
    oo_id = models.IntegerField(default=-1)

    name = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    birth = models.DateField()
    death = models.DateField(null=True, default=None, blank=True)
    portrait = models.URLField(max_length=200)
    biography = models.TextField(default="")

    country_ids = models.ManyToManyField(Country, blank=True)
    period_ids = models.ManyToManyField(Period, blank=True)

    is_popular = models.BooleanField(default=False)
    is_essential = models.BooleanField(default=False)

    slug = models.SlugField(max_length=255, unique=True, null=True)
    wikipedia_url = models.URLField(max_length=230, default="")

    def __str__(self):
        return str(self.name) + ", " + str(self.first_name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name) + " " + str(self.first_name))
        super(Composer, self).save(*args, **kwargs)


"""
    ********************************************
    ***           Works & Versions           ***
    ********************************************
"""


class Work(models.Model):
    oo_id = models.IntegerField(default=-1)
    oo_genre = models.CharField(max_length=40, default="")

    name = models.CharField(max_length=100)
    subname = models.CharField(max_length=100, default="")
    nickname = models.CharField(max_length=60, default="")
    composer_id = models.ForeignKey(Composer, on_delete=models.CASCADE, null=False)

    catalogue = models.CharField(max_length=20, default="")
    catalogue_number = models.IntegerField(default=0)
    
    # Stored as a char because it's more convenient. Sometimes we have to put "1849-1852" because composer was lazy
    date = models.CharField(max_length=30, default="")
    tonality = models.CharField(max_length=30, default="")

    is_popular = models.BooleanField(default=False)
    is_essential = models.BooleanField(default=False)

    slug = models.SlugField(max_length=255, unique=True, null=True)

    def __str__(self):
        return str(self.composer_id.name)[:15] + ": " + str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name) + "(" + str(self.composer_id.name) + " " + str(self.first_name) + ")")
        super(Work, self).save(*args, **kwargs)


class WorkVersion(models.Model):
    work_id = models.ForeignKey(Work, on_delete=models.CASCADE)
    is_original = models.BooleanField()
    performers_quantity = models.IntegerField(default=0, blank=True)

    alt_name = models.CharField(max_length=100, null=True, blank=True)
    alt_catalogue = models.CharField(max_length=20, null=True, blank=True)
    alt_catalogue_number = models.IntegerField(null=True, blank=True)
    alt_date = models.CharField(max_length=30, null=True, blank=True)
    alt_tonality = models.CharField(max_length=30, null=True, blank=True)
    
    arranger_id = models.ForeignKey(Composer, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    instruments_ids = models.ManyToManyField("Instrument", through="WorkVersionEnsemble")

    def __str__(self):
        return str(self.alt_name) if self.alt_name else str(self.work_id.name)

    # Called each time an instrument quantity is changed (in WorkVersionEnsemble)
    def compute_performers(self):
        self.performers_quantity = 0
        for instrument in self.workversionensemble_set.all():
            # We add the quantity only if it's not an ensemble (an orchestra doesn't count for example)
            if not instrument.instrument_id.is_ensemble:
                self.performers_quantity += instrument.quantity
        self.save()




"""
    ********************************************
    ***              Instrument              ***
    ********************************************
"""


class Instrument(models.Model):
    # Set to null if it's a root category
    parent_id = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, default=None, blank=True)
    name = models.CharField(max_length=60)
    sequence = models.IntegerField(default=1)

    key = models.CharField(max_length=10, default="C", blank=True)
    is_ensemble = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["parent_id__id", "sequence", "id"]



class WorkVersionEnsemble(models.Model):
    work_version_id = models.ForeignKey(WorkVersion, on_delete=models.CASCADE)
    instrument_id = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.work_version_id.alt_name) if self.work_version_id.alt_name else str(self.work_version_id.work_id.name)

    def save(self, *args, **kwargs):
        # We need to save this BEFORE computing performers quantity in corresponding Work Version
        super().save(*args, **kwargs)
        self.work_version_id.compute_performers()