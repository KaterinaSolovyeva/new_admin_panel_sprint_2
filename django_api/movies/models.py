import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0, message=_('Rating should be greater than 0')),
            MaxValueValidator(100, message=_('Rating should be less than 100'))
        ],
    )
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=FilmType.choices,
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name=_('genres'),
        through='GenreFilmwork',
        blank=True
    )
    people = models.ManyToManyField(
        Person,
        verbose_name=_('people'),
        through='PersonFilmwork',
        blank=True
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = (
            models.Index(fields=['creation_date', ]),
            models.Index(fields=['rating', ])
        )

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE,
        verbose_name=_('Filmwork'),
        db_index=False
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name=_('Genre'),
        db_index=False
    )
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='film_work_genre_idx'
            ),
        ]


class PersonFilmwork(UUIDMixin):
    class PersonRole(models.TextChoices):
        WRITER = 'writer', _('writer')
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')

    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE,
        verbose_name=_('Filmwork')
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        related_name='personfilmwork',
        verbose_name=_('Person')
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=PersonRole.choices,
        blank=False
    )
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_role_idx'
            ),
        ]
