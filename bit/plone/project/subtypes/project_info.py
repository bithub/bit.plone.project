from zope import interface
from zope.interface import implements

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import public as atapi

from p4a.subtyper import interfaces as stifaces

from bit.plone.project.interfaces import IProjectInfo
from bit.plone.project.subtypes.interfaces import IProjectInfoSubtype


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


class ExStringField(ExtensionField, atapi.StringField):
    """A trivial field."""


class ExTextField(ExtensionField, atapi.TextField):
    """A trivial field."""


class ExLinesField(ExtensionField, atapi.LinesField):
    """A trivial field."""


project_info_fields = [
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


class ProjectInfoExtender(object):
    implements(ISchemaExtender)
    fields = project_info_fields

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class ProjectInfo(object):
    implements(IProjectInfo)

    def __init__(self, context):
        self.context = context['info']
        self.project = context

    def set_project_email(self, email):
        return self.context.Schema()['project_email'].set(self.context, email)

    def get_project_email(self):
        return self.context.Schema()['project_email'].get(self.context)
    email = property(get_project_email, set_project_email)

    def get_project_phone(self):
        return self.context.Schema()['project_phone'].get(self.context)

    def set_project_phone(self, phone):
        return self.context.Schema()['project_phone'].set(self.context, phone)
    phone = property(get_project_phone, set_project_phone)

    def get_project_url(self):
        project_url = self.context.Schema(
            )['project_url'].get(self.context)
        return project_url or self.project.absolute_url()

    def set_project_url(self, url):
        return self.context.Schema()['project_url'].set(self.context, url)
    url = property(get_project_url, set_project_url)

    def get_project_address(self):
        project_address = self.context.Schema(
            )['project_address'].get(self.context)
        return project_address

    def set_project_address(self, address):
        return self.context.Schema(
            )['project_address'].set(self.context, address)
    address = property(get_project_address, set_project_address)

    def get_project_contacts(self):
        contacts = []
        membership = getToolByName(self.context, 'portal_membership')

        for memberid in self.context.Schema(
            )['project_contacts'].get(self.context):
            member = membership.getMemberById(memberid)
            if member:
                membername = member.getProperty(
                    'fullname') or member.getUserName()
                contacts.append('%s <%s>' % (
                        membername, member.getProperty('email')))

        contacts += ['%s <%s>' % (x.Title(), x.getRemoteUrl()) for x
                     in self.context.contentValues()
                     if x.portal_type == 'Link'
                     and not x.getRemoteUrl().startswith('http://')
                     and not x.getRemoteUrl().startswith('https://')
                     and '@' in x.getRemoteUrl()]
        return [self.email] + contacts
    contacts = property(get_project_contacts)

    def add_contact(self, userid):
        contacts = list(self.context.Schema(
            )['project_contacts'].get(self.context))
        contacts.append(userid)
        self.context.Schema(
            )['project_contacts'].set(self.context, contacts)

    def add_link(self, id, title, url):
        self.context.invokeFactory('Link', id)
        self.context[id].setTitle(title)
        self.context[id].setRemoteUrl(url)

    def get_project_links(self):
        links = [x.getRemoteUrl() for x
                 in self.context.contentValues()
                 if x.portal_type == 'Link'
                 and x.getRemoteUrl().startswith('http://')
                 or x.getRemoteUrl().startswith('https://')]
        project_urls = [self.url]
        if not project_urls == [self.project.absolute_url()]:
            project_urls.append(self.project.absolute_url())
        return project_urls + links
    links = property(get_project_links)
