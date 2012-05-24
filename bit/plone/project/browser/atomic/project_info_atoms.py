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
from bit.plone.atomic.adapters import PageLayout
from bit.plone.multiportlet.portlet.portlet_multi_portlet\
    import Assignment as multi_portlet
from bit.plone.project.interfaces\
    import IProject, IProjectNews, IProjectEvents
from bit.plone.project.subtypes.interfaces import IProjectInfoSubtype
from bit.plone.project.browser.portlets import portlet_project_info


class ProjectInfoPageLayout(PageLayout):
    adapts(IProjectInfoSubtype)

    def show_title(self):
        return True

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

    @property
    def project(self):
        return IProject(self._project())

    def _project(self):
        return self.context.aq_inner.aq_parent

    def _project_path(self, path=''):
        return '/%s' % '/'.join(list(
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
                    fragletShowTitle=False,
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
            'project-info',
            portlet_project_info.Assignment(path=self._project_path())
            )

        frag_paths = []
        excluded_folders = ['partners', 'media', 'info']
        for folder in self.project.get_project_folders(non_empty=True):
            if len(frag_paths) < 3:
                if not folder in excluded_folders:
                    frag_paths.append(folder)
            else:
                break

        mf = []
        subs = []
        for path in frag_paths:
            news = IProjectNews(
                self.project.get_project_folder(path), None)
            events = IProjectEvents(
                self.project.get_project_folder(path), None)
            css_class = 'overlayFragletItems medium-tall-box'
            fraglet_dict = dict(fragletPath=self._project_path(path),
                                fragletShowTitle=True,
                                fragletShowDescription=False,
                                fragletShowSummary=False,
                                fragletShowThumbnail=False,
                                fragletCssClass=css_class,
                                listingBatchResults=True,
                                listingItemsPerPage=5,
                                itemShowTitle=True,
                                itemShowIcon=True,
                                itemShowGraphic='tile',
                                itemShowSummary=False,
                                itemShowDescription=True,
                                itemShowDownloadLink=True)
            
            if events:
                fraglet_dict['itemProperties'] = 'timespan\nlongdate'
            if news:
                fraglet_dict['itemProperties'] =\
                    'effective: Published: $PROP\nCreator: by $PROP'
            subportlet = path.split('/')[-1]
            subs.append(subportlet)
            yield self.atomic(
                subportlet,
                fraglet(**fraglet_dict),
                hidden=True
                )
        yield self.atomic(
            'project-listings',
            multi_portlet(dict(portlets=subs,
                               portlet_type='tabbed')))

        media = self.project.get_project_folder('media')
        if media and media.contentIds():
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

    @property
    def _bottom(self):
        partners = self.project.get_project_folder('partners')
        if partners and partners.contentIds():
            yield self.atomic(
                'project-partners',
                fraglet(
                    fragletPath=self._project_path('partners'),
                    fragletShowTitle=False,
                    fragletShowDescription=False,
                    fragletShowSummary=False,
                    fragletShowThumbnail=False,
                    fragletCssClass='floatedBoxes',
                    listingBatchResults=True,
                    listingItemsPerPage=5,
                    itemShowTitle=False,
                    itemShowIcon=False,
                    itemShowGraphic='thumb',
                    itemShowSummary=False,
                    itemLinkDirectly=False,
                    itemShowDescription=False))


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
