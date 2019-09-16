from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from .config import GRADIENT_COLORS, PURPLE_GRADIENT, FLAT_COLORS, FLAT_BLACK, CONTENT_ALIGNMENT, ALIGN_RIGHT, SITE_BAR_TYPE, HEADER_BAR, FORM_TYPES, CONNECT_FORM


class ButtonBlock(blocks.StructBlock):
    button_color = blocks.ChoiceBlock(
        GRADIENT_COLORS, default=PURPLE_GRADIENT, required=False)
    title = blocks.CharBlock(max_length=100, required=False)
    link_external = blocks.URLBlock(required=False)
    document = DocumentChooserBlock(icon='doc-full', required=False)
    launch_form = blocks.ChoiceBlock(
        FORM_TYPES, default=CONNECT_FORM, required=False)

    class Meta:
        icon = 'link'


class ContentBlock(blocks.StructBlock):
    layout = blocks.ChoiceBlock(
        choices=CONTENT_ALIGNMENT, default=ALIGN_RIGHT)
    title = blocks.CharBlock(max_length=50, required=True)
    title_color = blocks.ChoiceBlock(FLAT_COLORS, FLAT_BLACK)
    description = blocks.RichTextBlock(required=False, blank=True, features=[
        'bold', 'italic', 'link', 'ul', 'ol'])
    image = ImageChooserBlock(required=True)
    button = ButtonBlock(required=False, blank=True)

    class Meta:
        icon = 'plus'


class KeyFeatureBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=True)
    title = blocks.CharBlock(max_length=50, required=True)
    title_color = blocks.ChoiceBlock(FLAT_COLORS, FLAT_BLACK)
    description = blocks.RichTextBlock(required=False, blank=True, features=[
                                       'bold', 'italic', 'link', 'ul', 'ol'])


class KeyFeaturesListBlock(blocks.StructBlock):
    feature_1 = KeyFeatureBlock()
    feature_2 = KeyFeatureBlock()
    feature_3 = KeyFeatureBlock()
    feature_4 = KeyFeatureBlock()


class HeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=True)
    title_color = blocks.ChoiceBlock(FLAT_COLORS, FLAT_BLACK)
    description = blocks.RichTextBlock(required=False, blank=True, features=[
        'bold', 'italic', 'link'])
    image = ImageChooserBlock(required=True)
    features = KeyFeaturesListBlock()
    button = ButtonBlock(required=False, blank=True)

    class Meta:
        icon = 'list'


class TextBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=True)
    title_color = blocks.ChoiceBlock(FLAT_COLORS, FLAT_BLACK)
    description = blocks.CharBlock(max_length=500, required=False)


class FeatureBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=True)
    title_color = blocks.ChoiceBlock(FLAT_COLORS, FLAT_BLACK)
    image = ImageChooserBlock(required=True)
    description = blocks.RichTextBlock(required=False, blank=True, features=[
                                       'bold', 'italic', 'link', 'ul', 'ol'])
    button = ButtonBlock(required=False, blank=True)


class FeatureSectionBlock(blocks.StructBlock):
    features = blocks.StreamBlock([('features', FeatureBlock())])

    class Meta:
        icon = 'list-ol'


class IntegrationLogo(blocks.StructBlock):
    company_name = blocks.CharBlock(max_length=100, required=True)
    logo = ImageChooserBlock(required=True)


class IntegrationListBlock(blocks.StructBlock):
    integrations = blocks.StreamBlock([('logo', IntegrationLogo())])


class SiteBarLink(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=False)
    title_color = blocks.ChoiceBlock(FLAT_COLORS, FLAT_BLACK)
    link_external = blocks.URLBlock(required=False)
    email = blocks.CharBlock(max_length=50, required=False)
    phone = blocks.CharBlock(max_length=20, required=False)


class SiteBarBlock(blocks.StructBlock):
    bar_type = blocks.ChoiceBlock(SITE_BAR_TYPE, HEADER_BAR)
    logo = ImageChooserBlock(required=False)
    link1 = SiteBarLink(required=False)
    link2 = SiteBarLink(required=False)
    link3 = SiteBarLink(required=False)


DEFAULT_CONTENT_BLOCKS = [
    ('content_block', ContentBlock()),
    ('integration_list', IntegrationListBlock()),
    ('text_block', TextBlock()),
    ('feature_section', FeatureSectionBlock())
]


class SectionContentBlock(blocks.StructBlock):
    integrator_block = blocks.StreamBlock(DEFAULT_CONTENT_BLOCKS)
    user_block = blocks.StreamBlock(DEFAULT_CONTENT_BLOCKS)
