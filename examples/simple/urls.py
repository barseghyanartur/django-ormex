from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

__all__ = ('urlpatterns',)

admin.autodiscover()

urlpatterns = []

urlpatterns_args = [
    # Admin URLs
    url(r'^admin/', include(admin.site.urls)),

    # Exercises URLs
    url(r'^exercises/', include('exercises.urls')),

    # Books URLs
    url(r'^books/', include('books.urls')),

    # Home page
    url(r'^$', TemplateView.as_view(template_name='home.html')),
]

urlpatterns += urlpatterns_args[:]

# Serving media and static in debug/developer mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    if settings.DEBUG_TOOLBAR is True:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
