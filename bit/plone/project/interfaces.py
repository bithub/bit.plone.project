import zope.schema
from zope.interface import Interface as I


class IProjectsTopic(I):

    def add_contacts_folder(self):
        pass


class IProjectMedia(I):

    def add_contact(self):
        pass

    def get_media(self):
        pass

    def get_emails(self):
        pass


class IProjectInfo(I):
    email = zope.schema.TextLine(title=(u"Email"))
    phone = zope.schema.TextLine(title=(u"Phone"))
    url = zope.schema.TextLine(title=(u"Url"))
    address = zope.schema.Text(title=(u"Postal address"))
    contacts = zope.schema.List(title=(u"Contacts"))
    links = zope.schema.List(title=(u"Links"))

    def add_contact(contact):
        pass

    def add_link(id, title, link):
        pass


class IProject(I):
    info = zope.schema.Object(title=(u"Info"),
                              schema=IProjectInfo)
    media = zope.schema.Object(title=(u"Media"),
                              schema=IProjectMedia)
    uid = zope.schema.TextLine(title=(u"Uid"))
    id = zope.schema.TextLine(title=(u"Id"))
    title = zope.schema.TextLine(title=(u"Title"))
    path = zope.schema.TextLine(title=(u"Path"))
    status = zope.schema.Choice(
        title=(u"Status"),
        vocabulary='bit.plone.project.vocabulary.ProjectStatus')

    # not so sure...
    def add_contacts_folder(self):
        pass

    def add_partners_folder(self):
        pass

    def get_project_status(self):
        pass

    def get_project_contacts(self):
        pass


class IProjectContacts(I):
    pass


class IProjectNews(I):

    def add_contact(self):
        pass

    def get_news(self):
        pass

    def get_emails(self):
        pass

    def get_links(self):
        pass


class IProjectLinks(I):

    def add_contact(self):
        pass

    def get_links(self):
        pass

    def get_emails(self):
        pass


class IProjectPartners(I):

    def add_contact(self):
        pass

    def get_partners(self):
        pass

    def get_emails(self):
        pass


class IProjectEvents(I):

    def add_contact(self):
        pass

    def get_events(self):
        pass

    def get_emails(self):
        pass

    def get_links(self):
        pass


class IProjectsFolder(I):

    def get_projects(self):
        pass
