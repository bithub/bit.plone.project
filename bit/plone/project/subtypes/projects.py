from zope import interface
from zope.interface import implements
from zope.component import getUtility

from p4a.subtyper import ISubtyper, interfaces as stifaces

from bit.plone.project.interfaces\
    import IProject, IProjectsFolder, IProjectContacts, IProjectInfo,\
    IProjectNews, IProjectContacts, IProjectLinks, IProjectEvents,\
    IProjectMedia

from bit.plone.project.subtypes.interfaces\
    import IProjectSubtype, IProjectContactsSubtype, IProjectInfoSubtype,\
    IProjectsFolderSubtype, IProjectNewsSubtype, IProjectLinksSubtype,\
    IProjectEventsSubtype, IProjectMediaSubtype


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
    default_view = 'info'
    allowed_types = ['Topic', 'Folder']
    also_provides = (IProjectsFolder, )
    permission = 'cmf.ManagePortal'


class Project(object):
    implements(IProject)

    def __init__(self, context):
        self.context = context

    def get_title(self):
        return self.context.Title()
    
    def add_contacts_folder(self):
        if not 'contacts' in self.context:
            self.context.invokeFactory('Folder', 'contacts')
        if not IProjectContacts(self.context['contacts'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(self.context['contacts'], 'bit.plone.project.ProjectContacts')

    def add_news_folder(self):
        if not 'news' in self.context:
            self.context.invokeFactory('Folder', 'news')
        if not IProjectNews(self.context['news'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(self.context['news'], 'bit.plone.project.ProjectNews')

    def add_links_folder(self):
        if not 'links' in self.context:
            self.context.invokeFactory('Folder', 'links')
        if not IProjectLinks(self.context['links'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(self.context['links'], 'bit.plone.project.ProjectLinks')

    def add_events_folder(self):
        if not 'events' in self.context:
            self.context.invokeFactory('Folder', 'events')
        if not IProjectEvents(self.context['events'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(self.context['events'], 'bit.plone.project.ProjectEvents')

    def add_info_folder(self):
        if not 'info' in self.context:
            self.context.invokeFactory('Folder', 'info')
        if not IProjectInfo(self.context['info'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(self.context['info'], 'bit.plone.project.ProjectInfo')

    def add_media_folder(self):
        if not 'media' in self.context:
            self.context.invokeFactory('Folder', 'media')
        if not IProjectMedia(self.context['media'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(self.context['media'], 'bit.plone.project.ProjectMedia')


class ProjectContacts(object):
    implements(IProjectContacts)

    def __init__(self, context):
        self.context = context
    
    def get_project_email(self):
        return 'project@3ca.org.uk'

    def get_project_url(self):
        return self.context.absolute_url()
        
    def get_project_contacts(self):
        links = [x.getRemoteUrl() for x in self.context['contacts'].contentValues()
                 if x.portal_type == 'Link'
                 and not x.getRemoteUrl().startswith('http://')
                 and not x.getRemoteUrl().startswith('https://')
                 and '@' in x.getRemoteUrl()]
        return links

    def get_project_links(self):
        links = [x.getRemoteUrl() for x in self.context['contacts'].contentValues()
                 if x.portal_type == 'Link'
                 and x.getRemoteUrl().startswith('http://')
                 or x.getRemoteUrl().startswith('https://')]
        return links


class ProjectMedia(object):
    implements(IProjectMedia)

    def get_project_galleries(self):
        pass

    def get_project_video(self):
        pass


class ProjectNews(object):
    implements(IProjectNews)

    def __init__(self, context):
        self.context = context
    
    def get_news(self):
        pass


class ProjectEvents(object):
    implements(IProjectEvents)

    def __init__(self, context):
        self.context = context
    
    def get_events(self):
        pass


class ProjectLinks(object):
    implements(IProjectLinks)

    def __init__(self, context):
        self.context = context
    
    def get_links(self):
        pass


class ProjectMedia(object):
    implements(IProjectMedia)

    def __init__(self, context):
        self.context = context
    
    def get_media(self):
        pass


class ProjectInfo(object):
    implements(IProjectInfo)

    def __init__(self, context):
        self.context = context
    
    def get_info(self):
        pass


class ProjectSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project'
    description = u'A project'
    type_interface = IProjectSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = 'info'
    permission = 'bit.plone.project.AddProject'


class ProjectContactsSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project contacts'
    description = u'Project contacts, URLs etc'
    type_interface = IProjectContactsSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectContacts'


class ProjectNewsSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project news'
    description = u'Project news, URLs etc'
    type_interface = IProjectNewsSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectNews'


class ProjectEventsSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project events'
    description = u'Project events, URLs etc'
    type_interface = IProjectEventsSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectEvents'


class ProjectLinksSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project links'
    description = u'Project links, URLs etc'
    type_interface = IProjectLinksSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectLinks'

class ProjectInfoSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project info'
    description = u'Project info, URLs etc'
    type_interface = IProjectInfoSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectInfo'


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
