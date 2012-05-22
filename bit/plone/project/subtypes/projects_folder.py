from zope import interface
from zope.interface import implements
from zope.event import notify

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import public as atapi
from Products.Archetypes.event import ObjectInitializedEvent

from p4a.subtyper import interfaces as stifaces

from bit.plone.project.interfaces\
    import IProjectsFolder, IProject

from bit.plone.project.subtypes.interfaces\
    import IProjectsFolderSubtype


class ExLinesField(ExtensionField, atapi.LinesField):
    """A trivial field."""

projects_folder_fields = [
    ExLinesField(
        "featured_content",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        widget=atapi.LinesWidget(
            label='Featured content',
            label_msgid='label_featured_content',
            description="Please enter the paths "\
                + "to featured projects or other content",
            description_msgid='help_featured_content',
            i18n_domain='plone',
            ),
        )
    ]


class ProjectsFolder(object):
    implements(IProjectsFolder)

    def __init__(self, context):
        self.context = context

    def add_project(self, project_id):
        project_folder = self.context[
            self.context.invokeFactory('Folder', project_id)]
        notify(ObjectInitializedEvent(project_folder))
        return IProject(project_folder)

    def get_featured_content(self):
        return self.context.Schema()['featured_content'].get(self.context)

    def get_projects_topics(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        topic_iface =\
            'bit.plone.project.subtypes.interfaces.IProjectsTopicSubtype'
        return [
            x.getId for x
            in portal_catalog.searchResults(
                sort_on='sortable_title',
                object_provides=topic_iface,
                path=self.get_path())]

    def get_path(self):
        return '/'.join(self.context.getPhysicalPath())

    def get_project(self, project_id):
        return IProject(self.context[project_id])

    def get_projects(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        project_iface =\
            'bit.plone.project.subtypes.interfaces.IProjectSubtype'
        return [
            x.getId for x
            in portal_catalog.searchResults(
                sort_on='sortable_title',
                object_provides=project_iface,
                path=self.get_path())]


class ProjectsFolderExtender(object):
    implements(ISchemaExtender)
    fields = projects_folder_fields

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class ProjectsFolderSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Projects folder'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Projects folder'
    description = u'A folder of projects'
    type_interface = IProjectsFolderSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Topic', 'Folder']
    permission = 'cmf.ManagePortal'
