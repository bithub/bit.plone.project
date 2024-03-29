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
from bit.plone.multiportlet.portlet.portlet_multi_portlet\
    import Assignment as multi_portlet
from bit.plone.atomic.adapters import PageLayout
from bit.plone.project.interfaces import IProjectsTopic
from bit.plone.project.subtypes.interfaces import IProjectsTopicSubtype


class ProjectsTopicPageLayout(PageLayout):
    adapts(IProjectsTopicSubtype)

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


class ProjectsTopicAtoms(FixedAtoms):

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
    def _right(self):
        projects = IProjectsTopic(self.context).get_projects_folder()
        topics = projects.get_projects_topics()
        for topic in topics:
            yield self.atomic(
                topic,
                fraglet(
                    fragletPath=self._project_path(topic),
                    fragletShowTitle=False,
                    fragletShowDescription=False,
                    fragletShowSummary=False,
                    fragletShowThumbnail=False,
                    fragletCssClass='tall-box',
                    listingBatchResults=True,
                    listingItemsPerPage=7,
                    itemShowTitle=True,
                    itemShowIcon=True,
                    itemShowGraphic='tile',
                    itemShowSummary=False,
                    itemShowDescription=True,
                    itemShowDownloadLink=True),
                hidden=True)
        yield self.atomic(
            'project-topics',
            multi_portlet(dict(portlets=topics,
                               portlet_type='tabbed')))


    @property
    def _left(self):
        featured_projects = IProjectsTopic(
            self.context).get_featured_projects()

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

        if not featured_projects:
            yield self.atomic(
                'projects',
                fraglet(fragletPath=".",
                        fragletShowTitle=False,
                        fragletShowDescription=False,
                        fragletShowSummary=False,
                        fragletShowThumbnail=False,
                        itemShowSummary=True,
                        itemShowDescription=True,
                        itemShowGraphic='mini',
                        listingMaxItems=0,
                        listingBatchItems=True,
                        listingItemsPerPage=3))
        else:
            for project in featured_projects:
                yield self.atomic(
                    'project-%s' % project,
                    fraglet(fragletPath=self._project_path(project),
                            fragletShowTitle=True,
                            fragletShowDescription=True,
                            fragletShowSummary=True,
                            fragletShowThumbnail=True,
                            itemShowSummary=True,
                            itemShowDescription=True,
                            itemShowGraphic='mini',
                            listingMaxItems=-1))


# should be able to get rid of this!
@adapter(IProjectsTopicSubtype, IPortletManager)
@implementer(IPortletAssignmentMapping)
def projectTopicAssignmentMappingAdapter(context, manager):
    assig = PortletAssignmentMapping(
        manager=manager.__name__, category='context')
    atoms = ProjectsTopicAtoms()
    atoms.context = context
    [assig._data.__setitem__(x['name'], x['assignment'])
     for x in atoms.getPortlets(manager.__name__)]
    return assig


class ProjectsTopicAtomicRetriever(
    FixedAtomicRetriever, ProjectsTopicAtoms):
    implements(IPortletRetriever)
    adapts(IProjectsTopicSubtype, IAtoms)
