from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField


from wagtail.admin.edit_handlers import (InlinePanel,
                                         FieldPanel,
                                         RichTextFieldPanel,
                                         StreamFieldPanel)

from .blocks import (HeroBlock, DEFAULT_CONTENT_BLOCKS, SiteBarBlock)


class LandingPage(Page):
    DEFAULT_VIEWS = (
        ('integrator', 'Integrator'),
        ('user', 'Daily User'),
    )
    hero = StreamField([('hero', HeroBlock())], null=True)
    default_view = models.CharField(
        max_length=12, choices=DEFAULT_VIEWS, default='integrator')
    integrator_sections = StreamField(
        DEFAULT_CONTENT_BLOCKS, null=True)
    user_sections = StreamField(
        DEFAULT_CONTENT_BLOCKS, null=True)
    site_bars = StreamField([('site_bars', SiteBarBlock())], null=True)

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('hero'),
        FieldPanel('default_view'),
        StreamFieldPanel('integrator_sections'),
        StreamFieldPanel('user_sections'),
        StreamFieldPanel('site_bars')
    ]
