from api import graphene_wagtail
from django.db import models
import graphene
from graphene import List, Schema, ObjectType, NonNull, ID
from graphene_django import DjangoObjectType
# from training_center.models import ClassPage, CoursePage, RelatedCourse
from wagtail.images.models import Image
from wagtail.core.templatetags.wagtailcore_tags import richtext
from pages.query import PageQuery


# def videos_resolver(root, info):
#     repr_video = []
#     for block in root.videos.stream_data:
#         block_type = block.get('type')
#         v = block.get('value')
#         repr_video.append(v)
#     return repr_video


# class Video(ObjectType):
#     poster = graphene.Field(graphene_wagtail.WagtailImageNode)
#     poster_title = graphene.String()
#     video_src = graphene.String()
#     action_title = graphene.String()
#     duration = graphene.String()

#     def resolve_poster(dict, info):
#         poster = Image.objects.get(pk=dict['poster'])
#         return poster

#     def resolve_poster_title(dict, info):
#         return dict['posterTitle']

#     def resolve_video_src(dict, info):
#         return dict['videoSrc']

#     def resolve_action_title(dict, info):
#         return dict['actionTitle']

#     def resolve_duration(dict, info):
#         return dict['duration']


# class ClassNode(DjangoObjectType):
#     videos = graphene.List(Video, resolver=videos_resolver)

#     class Meta:
#         model = ClassPage
#         only_fields = ['title', 'id', 'video', 'content', 'suggested_links']

#     def resolve_content(self, info):
#         return richtext(self.content)


# class CourseNode(DjangoObjectType):
#     videos = List(Video, resolver=videos_resolver)
#     related_classes = NonNull(List(NonNull(ClassNode)))

#     class Meta:
#         model = CoursePage

#     def resolve_related_classes(course, info):
#         courses = RelatedCourse.objects.filter(course=course)
#         return [c.attached_class for c in courses]

#     def resolve_content(self, info):
#         return richtext(self.content)


# # class TrainingCenterQuery(ObjectType):
# #     courses = NonNull(List(NonNull(CourseNode)))
# #     course = NonNull(CourseNode, id=NonNull(ID))
# #     Class = NonNull(ClassNode, id=NonNull(ID))
# #     related_class = NonNull(ClassNode, id=NonNull(ID))
# #     classes = NonNull(List(NonNull(ClassNode)))

# #     def resolve_classes(self, info):
# #         return ClassPage.objects.live()

# #     def resolve_Class(self, info, **kwargs):
# #         id = kwargs.get('id')

# #         if id is not None:
# #             return ClassPage.objects.get(pk=id)
# #         return None

# #     def resolve_courses(self, info):
# #         return CoursePage.objects.live()

# #     def resolve_course(self, info, **kwargs):
# #         id = kwargs.get('id')

# #         if id is not None:
# #             return CoursePage.objects.get(pk=id)

# #     def resolve_related_class(self, info):
# #         return ClassPage.objects.live()


class Query(
    PageQuery,
):
    pass


schema = Schema(query=Query)
