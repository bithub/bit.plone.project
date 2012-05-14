from zope.interface import implements
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.portlets import base

from bit.plone.project.interfaces import IProjectContacts, IProject
from bit.plone.project.browser.interfaces import\
    IProjectContactsPortlet, IProjectContactsPortletRenderer


class Assignment(base.Assignment):
    implements(IProjectContactsPortlet)
    title = u'Archive Entry Preview'


class Renderer(base.Renderer):
    implements(IProjectContactsPortletRenderer)
    _template = ViewPageTemplateFile('project_contacts.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.updated = False

    @property
    def project_contacts(self):
        return IProjectContacts(self.context.aq_inner.aq_parent)

    @property
    def project(self):
        return IProject(self.context.aq_inner.aq_parent)

    def showPortlet(self):
        return True

    def get_url(self):
        return self.project_contacts.get_project_url()

    def get_email(self):
        return self.project_contacts.get_project_email()

    def get_phone(self):
        return self.project_contacts.get_project_phone()

    def get_contacts(self):
        return self.project_contacts.get_project_contacts()

    def get_links(self):
        return self.project_contacts.get_project_links()

    def get_id(self):
        return ''

    def get_class(self):
        return ''

    def get_title(self):
        return self.project.get_title()

    def render(self):
        return xhtml_compress(self._template())


class AddForm(base.AddForm):
    form_fields = form.Fields(IProjectContactsPortlet)
    label = u"Add Archive Entry Preview Portlet"
    description = "An archive entry preview portlet."

    def create(self, data):
        return Assignment()
