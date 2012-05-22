from zope.interface import Interface as I
from zope import schema

from plone.portlets.interfaces import IPortletDataProvider


class IProjectInfoPortlet(IPortletDataProvider):
    """ Portlet for displaying a preview of an archive entry  """

    path = schema.ASCIILine(
        title=u'Path to project',
        default='.',
        required=True)


class IProjectInfoPortletRenderer(I):
    """ Portlet renderer for displaying a preview of an archive entry  """
