from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Picture(models.Model):
    DOG = 1
    CAT = 2
    ANIMAL_KIND_CHOICES = (
        (DOG, 'dog'),
        (CAT, 'cat'),
    )

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='pictures')
    animal_kind = models.IntegerField(choices=ANIMAL_KIND_CHOICES)
    photo = models.ImageField(upload_to='animals')
    is_promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "Hello"


class Comment(models.Model):
    author = models.ForeignKey(Author, related_name='comments')
    picture = models.ForeignKey(Picture, related_name='comments')
    comment = models.TextField()
    editors_note = models.TextField()
