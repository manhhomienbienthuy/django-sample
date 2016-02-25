from django.contrib import admin
from django.db.models import Count, Sum, Case, When, IntegerField
from django.utils.html import format_html

from .models import Picture, Author, Comment

from django.contrib.admin.views.main import ChangeList


class PicturesChangeList(ChangeList):

    def get_results(self, request):
        super(PicturesChangeList, self).get_results(request)
        totals = self.result_list.aggregate(
            dogs_count=Sum(Case(When(animal_kind=Picture.DOG, then=1),
                                output_field=IntegerField())),
            cats_count=Sum(Case(When(animal_kind=Picture.CAT, then=1),
                                output_field=IntegerField())))
        self.totals = totals


class ProductiveAuthorsFilter(admin.SimpleListFilter):
    parameter_name = 'is_productive'
    title = 'Productive author'
    YES, NO = 1, 0

    # Number of comments for an author to be considered a productive one
    THRESHOLD = 100

    def lookups(self, request, model_admin):
        return (
            (self.YES, 'yes'),
            (self.NO, 'no'),
        )

    def queryset(self, request, queryset):
        qs = queryset.annotate(Count('comments'))

        # Note the syntax. This way we avoid touching the queryset if our
        # filter is not used at all.
        if self.value() == self.YES:
            return qs.filter(comments__count__gte=self.THRESHOLD)
        if self.value() == self.NO:
            return qs.filter(comments__count__lt=self.THRESHOLD)

        return queryset


class PictureAdmin(admin.ModelAdmin):
    list_filter = [ProductiveAuthorsFilter]
    list_display = ('title', 'photo', 'animal_kind', 'author',
                    'is_promoted', 'object_link', 'mail_link')
    actions = ['promote', ]
    search_fields = ('title', 'author__name', 'comments__text', )

    def promote(self, request, queryset):
        queryset.update(is_promoted=True)
        self.message_user(request, 'The posts are promoted')
    promote.short_description = 'Promote the pictures'

    def object_link(self, item):
        url = item.get_absolute_url()
        return format_html('<a href="{url}">open</a>', url=url)
    object_link.short_description = 'View on site'

    def get_changelist(self, request):
        return PicturesChangeList

    def mail_link(self, obj):
        return format_html('<a href="abc">send mail</a>')
    mail_link.short_description = 'Show some love'
    mail_link.allow_tags = True

    def mail_view(self, request, *args, **kwargs):
        obj = get_object_or_404(Picture, pk=kwargs['pk'])
        send_mail('Feel the granny\'s love', 'Hey, she loves your pet!',
                  'granny@yoursite.com', [obj.author.email])
        self.message_user(request, 'The letter is on its way')
        return redirect(reverse('admin:myapp_picture_changelist'))


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('picture', 'author', 'editors_note')
    list_editable = ('editors_note', )


admin.site.register(Picture, PictureAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
