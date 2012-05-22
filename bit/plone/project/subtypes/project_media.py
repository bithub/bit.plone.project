from zope import interface
from zope.interface import implements

from p4a.subtyper import interfaces as stifaces

from bit.plone.project.interfaces import IProjectMedia
from bit.plone.project.subtypes.interfaces import IProjectMediaSubtype


class ProjectMediaSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project media'
    description = u'Project media, URLs etc'
    type_interface = IProjectMediaSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectMedia'


class ProjectMedia(object):
    implements(IProjectMedia)

    def __init__(self, context):
        self.context = context

    def get_media(self):
        pass
