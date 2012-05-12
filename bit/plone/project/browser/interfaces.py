from zope.interface import Interface as I

from plone.portlets.interfaces import IPortletDataProvider


class IProjectContactsPortlet(IPortletDataProvider):
    """ Portlet for displaying a preview of an archive entry  """


class IProjectContactsPortletRenderer(I):
    """ Portlet renderer for displaying a preview of an archive entry  """
