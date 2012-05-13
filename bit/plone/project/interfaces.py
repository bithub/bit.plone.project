from zope.interface import Interface as I


class IProject(I):

    def add_contacts_folder(self):
        pass

    def get_project_status(self):
        pass

    def get_project_contacts(self):
        pass


class IProjectContacts(I):

    def add_contact(self):
        pass

    def get_contacts(self):
        pass

    def get_emails(self):
        pass

    def get_links(self):
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


class IProjectInfo(I):

    def add_contact(self):
        pass

    def get_info(self):
        pass

    def get_emails(self):
        pass


class IProjectMedia(I):

    def add_contact(self):
        pass

    def get_media(self):
        pass

    def get_emails(self):
        pass


class IProjectLinks(I):

    def add_contact(self):
        pass

    def get_links(self):
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
