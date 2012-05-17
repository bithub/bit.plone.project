import os

from zope.interface import implements, implementer
from zope.component import adapts, adapter

from plone.portlets.interfaces import IPortletRetriever
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.storage import PortletAssignmentMapping

from Products.CMFCore.utils import getToolByName

from bit.plone.atomic.interfaces import IAtoms
from bit.plone.atomic.browser.forms.retriever\
    import FixedAtoms, FixedAtomicRetriever

from bit.plone.fraglets.browser.portlets.portlet_fraglet\
    import Assignment as fraglet
from bit.plone.fraglets.browser.portlets.portlet_multi_fraglet\
    import Assignment as multi_fraglet

from bit.plone.atomic.adapters import PageLayout

from bit.plone.project.interfaces import IProject, IProjectsFolder
from bit.plone.project.subtypes.interfaces import IProjectsFolderSubtype


class ProjectsFolderPageLayout(PageLayout):
    adapts(IProjectsFolderSubtype)

    def show_title(self):
        return True

    def show_description(self):
        return False

    def show_summary(self):
        return False

    def show_graphic(self):
        return False

    def css_class(self):
        return 'fixedWidth'

    def css_id(self):
        return ''


class ProjectsFolderAtoms(FixedAtoms):

    @property
    def project(self):
        return IProject(self._project())

    def _project(self):
        return self.context

    def _project_path(self, path=''):
        return '/'.join(list(
                getToolByName(
                    self.context, 'portal_url'
                    ).getRelativeContentPath(
                    self._project()
                    )) + path.split('/'))

    @property
    def _left(self):
        featured_content = IProjectsFolder(self.context).get_featured_content()
        yield self.atomic(
            'project',
            fraglet(fragletPath=".",
                    fragletShowTitle=False,
                    fragletShowDescription=True,
                    fragletShowSummary=True,
                    fragletShowThumbnail=True,
                    itemShowSummary=True,
                    itemShowDescription=True,
                    itemShowGraphic='mini',
                    listingMaxItems=-1))

        if not featured_content:
            yield self.atomic(
                'projects',
                fraglet(fragletPath=".",
                        fragletShowTitle=False,
                        fragletShowDescription=False,
                        fragletShowSummary=False,
                        fragletShowThumbnail=False,
                        itemShowSummary=False,
                        itemShowDescription=True,
                        itemShowGraphic='thumb',
                        listingMaxItems=0,
                        listingBatchItems=3))
        else:
            for project in featured_content:
                yield self.atomic(
                    'project-%s' % project,
                    fraglet(fragletPath=project,
                            fragletShowTitle=True,
                            fragletShowDescription=True,
                            fragletShowSummary=False,
                            fragletShowThumbnail=True,
                            itemShowSummary=True,
                            itemShowDescription=True,
                            itemShowGraphic='thumb',
                            listingMaxItems=-1))

        yield self.atomic(
            'support-us',
            fraglet(fragletPath="/about/support-us",
                    fragletShowTitle=True,
                    fragletShowDescription=True,
                    fragletShowSummary=False,
                    fragletShowThumbnail=False,
                    itemShowTitle=True,
                    itemShowIcon=False,
                    itemShowSummary=False,
                    itemShowDescription=True, 
                    itemShowGraphic='tile',
                    listingBatchResults=False))


    @property
    def _right(self):
        projects = IProjectsFolder(self.context)
        topics = projects.get_projects_topics()
        yield self.atomic(
            'project-topics',
            multi_fraglet(
                    [(topic,
                      dict(fragletPath=self._project_path(topic),
                           fragletShowTitle=True,
                           fragletShowDescription=False,
                           fragletShowSummary=False,
                           fragletShowThumbnail=False,
                           fragletCssClass='tall-box',
                           listingBatchResults=True,
                           listingItemsPerPage=10,
                           itemShowTitle=True,
                           itemShowIcon=True,
                           itemShowGraphic='tile',
                           itemShowSummary=False,
                           itemShowDescription=True,
                           itemShowDownloadLink=True))
                     for topic in topics]))

        # this needs cleaning up and moving!
        names = {'/events/upcoming': 'Events',
                 '/about/news/latest': 'News'}
        yield self.atomic(
            'site-news',
            multi_fraglet(
                    [(names[path],
                      dict(fragletPath=path,
                           fragletShowTitle=False,
                           fragletShowDescription=False,
                           fragletShowSummary=False,
                           fragletShowThumbnail=False,
                           fragletCssClass='tall-box',
                           listingBatchResults=True,
                           listingItemsPerPage=5,
                           itemShowTitle=True,
                           itemShowIcon=True,
                           itemShowGraphic='tile',
                           itemShowSummary=False,
                           itemShowDescription=True,
                           itemShowDownloadLink=True))
                     for path in ['/about/news/latest',
                                  '/events/upcoming',]]))

    @property
    def _bottom(self):
        yield self.atomic(
            'partners',
            fraglet(fragletPath="/about/partners-funders",
                    fragletShowTitle=True,
                    fragletShowDescription=False,
                    fragletShowSummary=False,
                    fragletShowThumbnail=False,
                    fragletCssClass='floatedBoxes',
                    itemShowTitle=False,
                    itemShowSummary=False,
                    itemShowDescription=False, 
                    itemShowGraphic='tile',
                    listingBatchResults=False))


# should be able to get rid of this!
@adapter(IProjectsFolderSubtype, IPortletManager)
@implementer(IPortletAssignmentMapping)
def projectsFolderAssignmentMappingAdapter(context, manager):
    assig = PortletAssignmentMapping(
        manager=manager.__name__, category='context')
    atoms = ProjectsFolderAtoms()
    atoms.context = context
    [assig._data.__setitem__(x['name'], x['assignment'])
     for x in atoms.getPortlets(manager.__name__)]
    return assig


class ProjectsFolderAtomicRetriever(
    FixedAtomicRetriever, ProjectsFolderAtoms):
    implements(IPortletRetriever)
    adapts(IProjectsFolderSubtype, IAtoms)
