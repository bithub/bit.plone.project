from Products.Five import BrowserView as FiveView

from bit.plone.project.interfaces import IProject


class ProjectView(FiveView):
    def create_project_folders(self):
        IProject(self.context).add_contacts_folder()
        IProject(self.context).add_news_folder()
        IProject(self.context).add_events_folder()
        IProject(self.context).add_links_folder()
        IProject(self.context).add_media_folder()
        IProject(self.context).add_info_folder()
        IProject(self.context).add_partners_folder()
