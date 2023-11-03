from django.contrib import admin
from .models import Tour, TourURL, TourOperator, Review

# Register your models here.
admin.site.register(Tour)
admin.site.register(TourOperator)


class TourURLAdmin(admin.ModelAdmin):
    list_display = ('shortened_url', 'stream', 'checked', 'success')
    list_filter = ('checked', 'success', 'stream')
    search_fields = ('url',)

    def shortened_url(self, obj):
        if len(obj.url) > 50:
            return obj.url[:50] + '...'
        return obj.url
    shortened_url.short_description = 'URL'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating', 'source_stream')
    list_filter = ('source_stream', )

admin.site.register(Review, ReviewAdmin)

admin.site.register(TourURL, TourURLAdmin)
