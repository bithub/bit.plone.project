from zope.interface import implements
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.portlets import base

from bit.plone.project.interfaces import IProject
from bit.plone.project.browser.interfaces import\
    IProjectInfoPortlet, IProjectInfoPortletRenderer


class Assignment(base.Assignment):
    implements(IProjectInfoPortlet)
    title = u'Archive Entry Preview'

    def __init__(self, path):
        self.path = path


class Renderer(base.Renderer):
    implements(IProjectInfoPortletRenderer)
    _template = ViewPageTemplateFile('project_info.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.updated = False

    @property
    def project(self):
        path = self.data.path
        if path.startswith('/'):
            target = self.context.portal_url.getPortalObject(
                ).restrictedTraverse(self.data.path[1:])
        else:
            target = self.context.restrictedTraverse(self.data.path)
        return IProject(target, None)

    def showPortlet(self):
        return self.project and True or False

    def status(self):
        status = self.project.status
        # this is a dirty hack...
        STATUS = dict(
            complete='This project is not currently running, '
            + 'but please contact us if you would like to see it happen again',
            occasional='This project is not currently running, '
            + 'but drop us an email and we\'ll let you know next time it is')
        if status in STATUS:
            return STATUS[status]
        return ''

    def get_id(self):
        return ''

    def get_class(self):
        return ''

    def get_title(self):
        return self.project.title

    def render(self):
        return xhtml_compress(self._template())


class AddForm(base.AddForm):
    form_fields = form.Fields(IProjectInfoPortlet)
    label = u"Add Archive Entry Preview Portlet"
    description = "An archive entry preview portlet."

    def create(self, data):
        return Assignment()
