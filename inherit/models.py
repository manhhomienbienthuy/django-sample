from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField


class ContentItemBase(models.Model):
    COMMENT_STATUS_CHOICES = (
        ('0', 'Open'),
        ('1', 'Closed'),
    )
    DEFAULT_COMMENT_STATUS = '0'
    CONTENT_STATUS_CHOICES = (
        ('1', 'Draft'),
        ('2', 'Public'),
    )
    DEFAULT_CONTENT_STATUS = '1'

    title = models.CharField(_('title'), max_length=100,
                             unique_for_date="publish_on")
    slug = models.SlugField(_('slug'))
    created_on = models.DateTimeField(_('created on'), auto_now_add=True,
                                      editable=False, )
    updated_on = models.DateTimeField(_('updated on'), editable=False)
    publish_on = models.DateTimeField(_('publish on'), )
    tags = TagField()
    status = models.IntegerField(
        _('status'),
        choices=CONTENT_STATUS_CHOICES,
        default=DEFAULT_CONTENT_STATUS,
        db_index=True
    )
    comment_status = models.IntegerField(
        _('comment status'),
        choices=COMMENT_STATUS_CHOICES,
        default=DEFAULT_COMMENT_STATUS,
        db_index=True
    )

    class Meta:
        abstract = True


class Post(ContentItemBase):
    DEFAULT_INPUT_FORMAT = 'X'
    INPUT_FORMAT_CHOICES = (
        ('X', 'XHTML'),
        ('M', 'Markdown'),
        ('R', 'Resructured Text'),
    )

    teaser = models.TextField(_('teaser'), blank=True, null=False)
