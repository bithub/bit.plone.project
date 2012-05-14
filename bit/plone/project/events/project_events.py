from zope.component import getUtility

from p4a.subtyper import ISubtyper

from bit.plone.project.interfaces import IProject
from bit.plone.project.subtypes.interfaces import IProjectsFolderSubtype


def add_project(obj, event):
    if IProjectsFolderSubtype.providedBy(obj.aq_inner.aq_parent):
        subtyper = getUtility(ISubtyper)
        subtyper.change_type(obj, 'bit.plone.project.Project')


def add_project_folders(obj, event):
    IProject(obj).add_contacts_folder()
    IProject(obj).add_news_folder()
    IProject(obj).add_events_folder()
    IProject(obj).add_links_folder()
    IProject(obj).add_media_folder()
    IProject(obj).add_info_folder()
    IProject(obj).add_partners_folder()
