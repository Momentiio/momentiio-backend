from django.db import models
from api import graphene_wagtail
import graphene
from graphene import NonNull, ObjectType, List, Field, String, Union
from graphene_django import DjangoObjectType
from wagtail.images.models import Image
from wagtail.core.templatetags.wagtailcore_tags import richtext
from .models import LandingPage


class Button(ObjectType):
    button_color = String()
    title = String()
    link_external = String()
    launch_form = String()

    def resolve_button_color(dict, info):
        return dict['button_color']

    def resolve_title(dict, info):
        return dict['title']

    def resolve_link_external(dict, info):
        return dict['link_external']

    def resolve_launch_form(dict, info):
        return dict['launch_form']


class ContentBlock(ObjectType):
    layout = NonNull(String)
    title = NonNull(String)
    title_color = String()
    description = String()
    image = NonNull(graphene_wagtail.WagtailImageNode)
    button = Field(Button)

    def resolve_layout(dict, info):
        return dict['layout']

    def resolve_title(dict, info):
        return dict['title']

    def resolve_title_color(dict, info):
        return dict['title_color']

    def resolve_description(dict, info):
        return dict['description']

    def resolve_image(dict, info):
        return Image.objects.get(pk=dict['image'])

    def resolve_button(dict, info):
        return dict['button']


class KeyFeature(ObjectType):
    icon = NonNull(graphene_wagtail.WagtailImageNode)
    title = NonNull(String)
    title_color = String()
    description = String()

    def resolve_icon(dict, info):
        return Image.objects.get(pk=dict['icon'])

    def resolve_title(dict, info):
        return dict['title']

    def resolve_title_color(dict, info):
        return dict['title_color']

    def resolve_description(dict, info):
        return dict['description']


class KeyFeaturesSection(ObjectType):
    feature_1 = NonNull(KeyFeature)
    feature_2 = NonNull(KeyFeature)
    feature_3 = NonNull(KeyFeature)
    feature_4 = NonNull(KeyFeature)

    def resolve_feature_1(dict, info):
        return dict['feature_1']

    def resolve_feature_2(dict, info):
        return dict['feature_2']

    def resolve_feature_3(dict, info):
        return dict['feature_3']

    def resolve_feature_4(dict, info):
        return dict['feature_4']


class Hero(ObjectType):
    title = NonNull(String)
    title_color = String()
    description = String()
    image = NonNull(graphene_wagtail.WagtailImageNode)
    features = NonNull(KeyFeaturesSection)
    button = Field(Button)

    def resolve_title(dict, info):
        return dict['title']

    def resolve_title_color(dict, info):
        return dict['title_color']

    def resolve_description(dict, info):
        return dict['description']

    def resolve_image(dict, info):
        return Image.objects.get(pk=dict['image'])

    def resolve_features(dict, info):
        return dict['features']

    def resolve_button(dict, info):
        return dict['button']


class TextBlock(ObjectType):
    title = NonNull(String)
    title_color = String()
    description = String()

    def resolve_title(dict, info):
        return dict['title']

    def resolve_title_color(dict, info):
        return dict['title_color']

    def resolve_description(dict, info):
        return dict['description']


class Feature(ObjectType):
    title = NonNull(String)
    title_color = String()
    image = NonNull(graphene_wagtail.WagtailImageNode)
    description = String()
    button = Field(Button)

    def resolve_title(dict, info):
        return dict['title']

    def resolve_title_color(dict, info):
        return dict['title_color']

    def resolve_image(dict, info):
        return Image.objects.get(pk=dict['image'])

    def resolve_description(dict, info):
        return dict['description']

    def resolve_button(dict, info):
        return dict['button']


class FeatureSection(ObjectType):
    features = NonNull(List(NonNull(Feature)))

    def resolve_features(dict, info):
        return [feature.get('value') for feature in dict['features']]


class IntegrationLogo(ObjectType):
    company_name = NonNull(String)
    logo = NonNull(graphene_wagtail.WagtailImageNode)

    def resolve_company_name(dict, info):
        return dict['company_name']

    def resolve_logo(dict, info):
        return Image.objects.get(pk=dict['logo'])


class IntegrationListBlock(ObjectType):
    integrations = NonNull(List(NonNull(IntegrationLogo)))

    def resolve_integrations(dict, info):
        return [integration.get('value') for integration in dict['integrations']]


class SiteBarLink(ObjectType):
    title = NonNull(String)
    title_color = NonNull(String)
    link_external = String()
    email = String()
    phone = String()

    def resolve_title(dict, info):
        return dict['title']

    def resolve_title_color(dict, info):
        return dict['title_color']

    def resolve_link_external(dict, info):
        return dict['link_external']

    def resolve_email(dict, info):
        return dict['email']

    def resolve_phone(dict, info):
        return dict['phone']


class SiteBarBlock(ObjectType):
    bar_type = NonNull(String)
    logo = NonNull(graphene_wagtail.WagtailImageNode)
    link1 = Field(SiteBarLink)
    link2 = Field(SiteBarLink)
    link3 = Field(SiteBarLink)

    def resolve_bar_type(dict, info):
        return dict['bar_type']

    def resolve_logo(dict, info):
        return Image.objects.get(pk=dict['logo'])

    def resolve_link1(dict, info):
        return dict['link1']

    def resolve_link2(dict, info):
        return dict['link2']

    def resolve_link3(dict, info):
        return dict['link3']


class Section(Union):
    class Meta:
        types = (ContentBlock, FeatureSection, IntegrationListBlock, TextBlock)

    @staticmethod
    def resolve_type(obj, info):
        if obj.get('type') == 'content_block':
            return ContentBlock
        elif obj.get('type') == 'integration_list_block':
            return IntegrationListBlock
        elif obj.get('type') == 'text_block':
            return TextBlock
        elif obj.get('type') == 'feature_section':
            return FeatureSection


class Page(DjangoObjectType):
    hero = NonNull(Hero)
    integrator_sections = NonNull(List(NonNull(Section)))
    user_sections = NonNull(List(NonNull(Section)))
    site_bars = NonNull(List(NonNull(SiteBarBlock)))

    class Meta:
        model = LandingPage
        only_fields = ['id', 'title', 'default_view']

    def resolve_hero(page, info):
        return page.hero.stream_data[0].get('value')

    def resolve_integrator_sections(page, info):
        return [{**section.get('value'), 'type': section.get('type')} for section in page.integrator_sections.stream_data]

    def resolve_user_sections(page, info):
        return [{**section.get('value'), 'type': section.get('type')} for section in page.user_sections.stream_data]

    def resolve_site_bars(page, info):
        return [{**bar.get('value'), 'type': bar.get('type')} for bar in page.site_bars.stream_data]


class PageQuery(ObjectType):
    page = NonNull(List(Page))

    def resolve_page(self, info):
        return LandingPage.objects.live()
