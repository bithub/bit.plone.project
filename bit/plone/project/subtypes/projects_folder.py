from zope import interface
from zope.interface import implements
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName

from p4a.subtyper import ISubtyper, interfaces as stifaces

from bit.plone.project.interfaces\
    import IProjectsFolder

from bit.plone.project.subtypes.interfaces\
    import IProjectsFolderSubtype


class ProjectsFolder(object):
    implements(IProjectsFolder)

    def __init__(self, context):
        self.context = context

    def get_projects_topics(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        topic_iface =\
            'bit.plone.project.subtypes.interfaces.IProjectsTopicSubtype'
        return [
            x.getId for x
            in portal_catalog.searchResults(
                object_provides=topic_iface,
                path=self.get_path())]

    def get_path(self):
        portal_url = getToolByName(self.context, 'portal_url')
        return '/'.join(self.context.getPhysicalPath())


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
