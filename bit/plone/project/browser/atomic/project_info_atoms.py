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
        return 'fancyRight fixedWidth'

    def css_id(self):
        return ''


class ProjectInfoAtoms(FixedAtoms):

    @property
    def _right(self):

        fraglet_path = '/'.join(getToolByName(
                self.context, 'portal_url').getRelativeContentPath(
                self.context.aq_inner.aq_parent))            
        yield self.atomic(
            'project-contacts',
            portlet_project_contacts.Assignment()           
            )
        yield self.atomic(
            'project-listing',
            fraglet(fragletPath=fraglet_path,
                    fragletShowTitle=True,
                    fragletShowDescription=True,
                    fragletShowSummary=False,
                    fragletShowThumbnail=False,
                    fragletCssClass='overlayFragletItems fixedWidth',
                    listingBatchResults=True,
                    listingItemsPerPage=5,
                    itemShowTitle=True,
                    itemShowIcon=True,
                    itemShowGraphic='thumb',
                    itemShowSummary=True,
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
