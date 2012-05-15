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

from bit.plone.project.subtypes.interfaces import IProjectInfoSubtype
from bit.plone.project.browser.portlets import portlet_project_contacts


class ProjectInfoPageLayout(PageLayout):
    adapts(IProjectInfoSubtype)

    def show_title(self):
        return False

    def show_description(self):
        return False

    def show_summary(self):
        return False

    def show_graphic(self):
        return False

    def css_class(self):
        return 'fixedWidth fatLeft'

    def css_id(self):
        return ''


class ProjectInfoAtoms(FixedAtoms):

    def _project(self):
        return self.context.aq_inner.aq_parent

    def _project_path(self, path=''):
        return '/'.join(list(
                getToolByName(
                    self.context, 'portal_url'
                    ).getRelativeContentPath(
                    self._project()
                    )) + path.split('/'))

    @property
    def _left(self):
        yield self.atomic(
            'project-summary',
            fraglet(fragletPath=self._project_path(),
                    fragletShowTitle=True,
                    fragletShowDescription=True,
                    fragletShowSummary=True,
                    fragletShowThumbnail=True,
                    listingMaxItems=-1))
        features = self._project().Schema(
            )['project_features'].get(self._project())
        for feature_path in features:
            yield self.atomic(
                'project-%s' % os.path.basename(feature_path),
                fraglet(fragletPath=feature_path,
                        fragletShowTitle=True,
                        fragletShowDescription=True,
                        fragletShowSummary=True,
                        fragletShowThumbnail=True,
                        listingMaxItems=-1))

    @property
    def _right(self):
        yield self.atomic(
            'project-contacts',
            portlet_project_contacts.Assignment()
            )
        frag_paths = ['news', 'events', 'links']

        yield self.atomic(
            'project-info',
            multi_fraglet(
                    [(frag,
                      dict(fragletPath=self._project_path(frag),
                           fragletShowTitle=False,
                           fragletShowDescription=False,
                           fragletShowSummary=False,
                           fragletShowThumbnail=False,
                           fragletCssClass='overlayFragletItems medium-tall-box',
                           listingBatchResults=True,
                           listingItemsPerPage=5,
                           itemShowTitle=True,
                           itemShowIcon=True,
                           itemShowGraphic='tile',
                           itemShowSummary=False,
                           itemShowDescription=True,
                           itemShowDownloadLink=True))
                     for frag in frag_paths]))

        yield self.atomic(
            'project-media',
            fraglet(
                fragletPath=self._project_path('media'),
                fragletShowTitle=True,
                fragletShowDescription=False,
                fragletShowSummary=False,
                fragletShowThumbnail=False,
                fragletCssClass='overlayFragletItems',
                listingBatchResults=True,
                listingItemsPerPage=5,
                itemShowTitle=True,
                itemShowIcon=True,
                itemShowGraphic='tile',
                itemShowSummary=False,
                itemLinkDirectly=False,
                itemShowDescription=True,
                itemShowDownloadLink=True))


# should be able to get rid of this!
@adapter(IProjectInfoSubtype, IPortletManager)
@implementer(IPortletAssignmentMapping)
def projectInfoAssignmentMappingAdapter(context, manager):
    assig = PortletAssignmentMapping(
        manager=manager.__name__, category='context')
    atoms = ProjectInfoAtoms()
    atoms.context = context
    [assig._data.__setitem__(x['name'], x['assignment'])
     for x in atoms.getPortlets(manager.__name__)]
    return assig


class ProjectInfoAtomicRetriever(
    FixedAtomicRetriever, ProjectInfoAtoms):
    implements(IPortletRetriever)
    adapts(IProjectInfoSubtype, IAtoms)
