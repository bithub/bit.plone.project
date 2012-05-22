from zope import interface
from zope.interface import implements
from zope.component import getUtility

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import public as atapi

from p4a.subtyper import ISubtyper, interfaces as stifaces

from bit.plone.fraglets.interfaces import IFolderResults
from bit.plone.project.interfaces\
    import IProject, IProjectContacts, IProjectInfo,\
    IProjectNews, IProjectLinks, IProjectEvents, IProjectMedia,\
    IProjectPartners
from bit.plone.project.subtypes.interfaces\
    import IProjectSubtype,\
    IProjectNewsSubtype, IProjectLinksSubtype,\
    IProjectEventsSubtype, IProjectPartnersSubtype


class ExStringField(ExtensionField, atapi.StringField):
    """A trivial field."""


class ExTextField(ExtensionField, atapi.TextField):
    """A trivial field."""


class ExLinesField(ExtensionField, atapi.LinesField):
    """A trivial field."""

project_fields = [
    ExStringField(
        "project_status",
        default='active',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        vocabulary_factory='bit.plone.project.vocabulary.ProjectStatus',
        widget=atapi.SelectionWidget(
            label='Project Status',
            label_msgid='label_project_status',
            description="Please enter the primary "\
                + "STATUS for this project, leave blank to use this STATUS",
            description_msgid='help_project_status',
            i18n_domain='plone',
            ),
        ),
    ExLinesField(
        "project_features",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        widget=atapi.LinesWidget(
            label='Project features',
            label_msgid='label_project_features',
            description="Please enter the paths "\
                + "to featured content for this project",
            description_msgid='help_project_features',
            i18n_domain='plone',
            ),
        ),
    ]


class ProjectExtender(object):
    implements(ISchemaExtender)
    fields = project_fields

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class Project(object):
    implements(IProject)

    def __init__(self, context):
        self.context = context

    def __eq__(self, other):
        if self.context == other.context:
            return True
        return False

    def get_uid(self):
        return self.context.UID()
    uid = property(get_uid)

    def get_id(self):
        return self.context.getId()
    id = property(get_id)

    def get_title(self):
        return self.context.Title()

    def set_title(self, title):
        return self.context.setTitle(title)
    title = property(get_title, set_title)

    def get_project_folder(self, folderid):
        if hasattr(self.context, folderid):
            # this should return an adapted folder...
            return self.context[folderid]

    def get_project_folders(self, non_empty=False):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        catalog_results = portal_catalog.searchResults(
            show_inactive=False,
            show_all=False,
            exclude_from_nav=False)
        for folder in [
            x for x
            in portal_catalog.searchResults(
                is_folderish=True,
                exclude_from_nav=False,
                path={
                    'query': self.get_path(),
                    'depth': 1},
                sort_on='getObjPositionInParent')
            ]:
            if non_empty:
                has_children = [
                    x.getPath() for x
                    in catalog_results
                    if not x.getPath() == folder.getPath()
                    and x.getPath().startswith(folder.getPath())
                    and not '/' in x.getPath().split(
                        folder.getPath())[1].lstrip('/')]
                if has_children:
                    yield folder.getId
            else:
                yield folder.getId

    def get_project_status(self):
        project_status = self.context.Schema(
            )['project_status'].get(self.context)
        return project_status

    def set_project_status(self, status):
        self.context.Schema(
            )['project_status'].set(self.context, status)
    status = property(get_project_status, set_project_status)

    def get_path(self):
        return '/'.join(self.context.getPhysicalPath())
    path = property(get_path)

    def get_info(self):
        return IProjectInfo(self.context)
    info = property(get_info)

    def get_media(self):
        return IProjectMedia(self.context)
    media = property(get_media)

    def add_contacts_folder(self):
        if not 'contacts' in self.context:
            self.context.invokeFactory('Folder', 'contacts')
        if not IProjectContacts(self.context['contacts'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['contacts'],
                'bit.plone.project.ProjectContacts')
        self.context['contacts'].setTitle('Contacts')

    def add_news_folder(self):
        if not 'news' in self.context:
            self.context.invokeFactory('Folder', 'news')
        if not IProjectNews(self.context['news'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['news'],
                'bit.plone.project.ProjectNews')
        self.context['news'].setTitle('News')

    def add_links_folder(self):
        if not 'links' in self.context:
            self.context.invokeFactory('Folder', 'links')
        if not IProjectLinks(self.context['links'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['links'],
                'bit.plone.project.ProjectLinks')
        self.context['links'].setTitle('Links')

    def add_partners_folder(self):
        if not 'partners' in self.context:
            self.context.invokeFactory('Folder', 'partners')
        if not IProjectPartners(self.context['partners'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['partners'],
                'bit.plone.project.ProjectPartners')
        self.context['partners'].setTitle('Partners')

    def add_events_folder(self):
        if not 'events' in self.context:
            self.context.invokeFactory('Folder', 'events')
        if not IProjectEvents(self.context['events'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['events'],
                'bit.plone.project.ProjectEvents')
        self.context['events'].setTitle('Events')

    def add_info_folder(self):
        if not 'info' in self.context:
            self.context.invokeFactory('Folder', 'info')
        if not IProjectInfo(self.context['info'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['info'],
                'bit.plone.project.ProjectInfo')
        self.context['info'].setTitle('Info')

    def add_media_folder(self):
        if not 'media' in self.context:
            self.context.invokeFactory('Folder', 'media')
        if not IProjectMedia(self.context['media'], None):
            subtyper = getUtility(ISubtyper)
            subtyper.change_type(
                self.context['media'],
                'bit.plone.project.ProjectMedia')
        self.context['media'].setTitle('Media')


class ProjectNews(object):
    implements(IProjectNews)

    def __init__(self, context):
        self.context = context

    def get_news(self, **kwa):
        content_filter = {}
        content_filter['path'] = dict(
            query=self.get_path(),
            depth=-1)
        content_filter['portal_type'] = 'News Item'
        content_filter['sort_on'] = 'effective'
        content_filter['sort_order'] = 'descending'
        max_items = kwa.get('max_items')
        if int(max_items or 0) == -1:
            return []
        return IFolderResults(self.context).get_results(
            contentFilter=content_filter,
            **kwa)

    def get_path(self):
        return '/'.join(self.context.getPhysicalPath())


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

    def get_links(self, **kwa):
        content_filter = {}
        content_filter['path'] = dict(
            query=self.get_path(),
            depth=-1)
        content_filter['portal_type'] = 'Link'
        content_filter['sort_on'] = 'effective'
        kwa['sort_on'] = 'effective'
        max_items = kwa.get('max_items')
        if int(max_items or 0) == -1:
            return []
        return IFolderResults(self.context).get_results(
            contentFilter=content_filter,
            **kwa)

    def get_path(self):
        return '/'.join(self.context.getPhysicalPath())


class ProjectPartners(object):
    implements(IProjectPartners)

    def __init__(self, context):
        self.context = context

    def get_partners(self):
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


class ProjectPartnersSubtype(object):
    """A descriptor for the ultra doc subtype.
    >>> descriptor = UltraDocDescriptor()
    >>> descriptor.title
    u'Project'
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Project partners'
    description = u'Project partners, URLs etc'
    type_interface = IProjectPartnersSubtype
    for_portal_type = 'Folder'
    icon = 'trinity-favicon-tiny.png'
    default_view = '@@atomic-view'
    allowed_types = ['Link']
    permission = 'bit.plone.project.AddProjectPartners'


class ProjectLinksResultsDelegation(object):

    def __init__(self, context):
        self.context = context

    def getResults(self, **kwa):
        return IProjectLinks(self.context).get_links(**kwa)


class ProjectNewsResultsDelegation(object):

    def __init__(self, context):
        self.context = context

    def getResults(self, **kwa):
        return IProjectNews(self.context).get_news(**kwa)
