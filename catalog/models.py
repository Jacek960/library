import uuid

from django.db import models

# Create your models here.
from django.utils.text import slugify


class Autor(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name.lower().replace('ł', 'l'))
        super(Autor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name.lower().replace('ł', 'l'))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='ad_image/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug  and self.title and self.autor:
            self.slug = slugify(f"{self.title.lower().replace('ł', 'l')}-{self.autor.slug}")
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'