from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import gettext_lazy as _
from rangefilter.filter import DateRangeFilter

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork

ModelAdmin.empty_value_display = _('-empty-')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ['name']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at', 'updated_at')
    search_fields = ('full_name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ['full_name']


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name = _("Filmwork's genre")
    verbose_name_plural = _("Filmwork's genres")


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person']
    verbose_name = _('Person in filmwork')
    verbose_name_plural = _('People in filmwork')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title', 'type', 'creation_date',
        'rating', 'get_genres', 'get_people', 'created_at', 'updated_at'
    )
    list_filter = ('type', ('creation_date', DateRangeFilter), 'genres')
    search_fields = ('title', 'description', 'id')

    def get_genres(self, obj):
        return ', '.join(
            [str(genre) for genre in obj.genres.all()]
        )
    get_genres.short_description = _('genres')

    def get_people(self, obj):
        return ', '.join(
            [str(person) for person in obj.people.all()]
        )
    get_people.short_description = _('people')
