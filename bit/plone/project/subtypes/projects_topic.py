from zope import interface
from zope.interface import implements

from p4a.subtyper import interfaces as stifaces

from bit.plone.fraglets.interfaces import ICollectionResults
from bit.plone.project.interfaces\
    import IProjectsTopic, IProjectsFolder
from bit.plone.project.subtypes.interfaces\
    import IProjectsTopicSubtype


class ProjectsTopic(object):
    implements(IProjectsTopic)

    def __init__(self, context):
        self.context = context

    def get_title(self):
        return self.context.Title()

    def get_projects_folder(self):
        return IProjectsFolder(self.context.aq_inner.aq_parent)


class ProjectsTopicSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project topic'
    """
    interface.implements(stifaces.IPortalTypedDescriptor)
    title = u'Project topic'
    description = u'A project topic'
    type_interface = IProjectsTopicSubtype
    for_portal_type = 'Topic'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    permission = 'bit.plone.project.AddProjectsTopic'


class ProjectsTopicResultsDelegation(object):

    def __init__(self, context):
        self.context = context

    def getResults(self, **kwa):
        project_iface = 'bit.plone.project.subtypes.interfaces.IProjectSubtype'
        projects = IProjectsTopic(self.context).get_projects_folder()
        kwa['object_provides'] = project_iface
        kwa['path'] = projects.get_path()
        max_items = kwa.get('max_items')
        if int(max_items or 0) == -1:
            return []
        return ICollectionResults(self.context).queryCatalog(**kwa)
