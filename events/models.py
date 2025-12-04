from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    # Categorías del evento
    CATEGORY_GAMING = 'gaming'
    CATEGORY_MUSIC = 'music'
    CATEGORY_TALK = 'talk'
    CATEGORY_EDUCATION = 'education'

    CATEGORY_CHOICES = [
        (CATEGORY_GAMING, 'Gaming'),
        (CATEGORY_MUSIC, 'Música'),
        (CATEGORY_TALK, 'Charla / Talk'),
        (CATEGORY_EDUCATION, 'Educación / Taller'),
    ]

    # Dificultad
    DIFFICULTY_BEGINNER = 'beginner'
    DIFFICULTY_INTERMEDIATE = 'intermediate'
    DIFFICULTY_ADVANCED = 'advanced'

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_BEGINNER, 'Principiante'),
        (DIFFICULTY_INTERMEDIATE, 'Intermedio'),
        (DIFFICULTY_ADVANCED, 'Avanzado'),
    ]

    # Estado
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_LIVE = 'live'
    STATUS_FINISHED = 'finished'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Borrador'),
        (STATUS_SCHEDULED, 'Programado'),
        (STATUS_LIVE, 'En directo'),
        (STATUS_FINISHED, 'Finalizado'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]

    # Duración por defecto según categoría (minutos)
    DEFAULT_DURATION_BY_CATEGORY = {
        CATEGORY_GAMING: 120,     # 2 horas
        CATEGORY_MUSIC: 90,       # 1,5 horas
        CATEGORY_TALK: 60,        # 1 hora
        CATEGORY_EDUCATION: 120,  # 2 horas
    }

    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    description = models.TextField(
        verbose_name='Descripción'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Categoría'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_BEGINNER,
        verbose_name='Nivel'
    )
    scheduled_for = models.DateTimeField(
        verbose_name='Fecha y hora programada'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name='Estado'
    )
    thumbnail = models.ImageField(
        upload_to='events/thumbnails/',
        blank=True,
        null=True,
        verbose_name='Imagen de portada'
    )
    max_viewers = models.PositiveIntegerField(
        default=100,
        verbose_name='Máximo de espectadores'
    )
    duration_minutes = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Duración prevista (minutos)'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Etiquetas (separadas por comas)',
        help_text='Ejemplo: python, django, streaming'
    )
    stream_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='URL del streaming / demo'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Evento destacado'
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Creador'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creado'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Actualizado'
    )

    class Meta:
        ordering = ['-scheduled_for', '-created_at']
        verbose_name = 'evento'
        verbose_name_plural = 'eventos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Si no hay duración, asignamos la duración por defecto según categoría
        if not self.duration_minutes and self.category in self.DEFAULT_DURATION_BY_CATEGORY:
            self.duration_minutes = self.DEFAULT_DURATION_BY_CATEGORY[self.category]
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        return self.scheduled_for < timezone.now()

    @property
    def is_upcoming(self):
        return self.scheduled_for >= timezone.now()
