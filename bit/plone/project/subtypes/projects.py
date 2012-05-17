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
    import IProjectSubtype, IProjectContactsSubtype, IProjectInfoSubtype,\
    IProjectNewsSubtype, IProjectLinksSubtype,\
    IProjectEventsSubtype, IProjectMediaSubtype, IProjectPartnersSubtype


class ExStringField(ExtensionField, atapi.StringField):
    """A trivial field."""


class ExTextField(ExtensionField, atapi.TextField):
    """A trivial field."""


class ExLinesField(ExtensionField, atapi.LinesField):
    """A trivial field."""

project_fields = [
    ExStringField(
        "project_email",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        widget=atapi.StringWidget(
            label='Project Email',
            label_msgid='label_project_email',
            description="Please enter the primary "\
                + "contact email for this project",
            description_msgid='help_project_email',
            i18n_domain='plone',
            ),
        ),
    ExTextField(
        "project_address",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        default_content_type='text/plain',
        default_output_type='text/plain',
        allowable_content_types=('text/plain'),
        widget=atapi.TextAreaWidget(
            label='Project Address',
            label_msgid='label_project_address',
            description="Please enter the primary "\
                + "contact address for this project",
            description_msgid='help_project_address',
            i18n_domain='plone',
            ),
        ),
    ExStringField(
        "project_url",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        widget=atapi.StringWidget(
            label='Project URL',
            label_msgid='label_project_url',
            description="Please enter the primary "\
                + "URL for this project, leave blank to use this URL",
            description_msgid='help_project_url',
            i18n_domain='plone',
            ),
        ),
    ExStringField(
        "project_phone",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        widget=atapi.StringWidget(
            label='Project phone',
            label_msgid='label_project_phone',
            description="Please enter the primary "\
                + "phone for this project, leave blank to use this phone",
            description_msgid='help_project_phone',
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
    ExLinesField(
        "project_contacts",
        default='',
        mode='rw',
        read_permission='zope.View',
        write_permission='cmf.ModifyPortalContent',
        widget=atapi.LinesWidget(
            label='Project Contacts',
            label_msgid='label_project_contacts',
            description="Please enter the user ids "\
                + "of the contacts for this project",
            description_msgid='help_project_contacts',
            i18n_domain='plone',
            ),
        )
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

    def get_title(self):
        return self.context.Title()

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

    def get_path(self):
        return '/'.join(self.context.getPhysicalPath())

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


class ProjectContacts(object):
    implements(IProjectContacts)

    def __init__(self, context):
        self.context = context

    def get_project_email(self):
        return self.context.Schema()['project_email'].get(self.context)

    def get_project_phone(self):
        return self.context.Schema()['project_phone'].get(self.context)

    def get_project_url(self):
        project_url = self.context.Schema(
            )['project_url'].get(self.context)
        return project_url or self.context.absolute_url()

    def get_project_address(self):
        project_address = self.context.Schema(
            )['project_address'].get(self.context)
        return project_address

    def get_project_contacts(self):
        contacts = []
        membership = getToolByName(self.context, 'portal_membership')

        # this is trinity specific...
        for member in self.context.Schema(
            )['project_contacts'].get(self.context):
            name = membership.getMemberById(member).getFullname()
            contacts.append('%s <%s@3ca.org.uk>' % (name, member))

        if 'contacts' in self.context:
            contacts += ['%s <%s>' % (x.Title, x.getRemoteUrl()) for x
                         in self.context['contacts'].contentValues()
                         if x.portal_type == 'Link'
                         and not x.getRemoteUrl().startswith('http://')
                         and not x.getRemoteUrl().startswith('https://')
                         and '@' in x.getRemoteUrl()]
        return contacts

    def get_project_links(self):
        links = [x.getRemoteUrl() for x
                 in self.context['contacts'].contentValues()
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

    def get_links(self, **kwa):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        content_filter = {}
        content_filter['path'] = dict(
            query=self.get_path(),
            depth=-1)
        content_filter['portal_type'] = 'Link'
        content_filter['sort_on'] = 'effective'
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


class ProjectLinksResultsDelegation(object):

    def __init__(self, context):
        self.context = context

    def getResults(self, **kwa):
        return IProjectLinks(self.context).get_links(**kwa)
