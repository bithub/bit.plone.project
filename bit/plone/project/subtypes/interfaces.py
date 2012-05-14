from zope.interface import alsoProvides
from zope.app.content.interfaces import IContentType

from p4a.subtyper.interfaces import ISubtyped


class IProjectSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectSubtype, IContentType)


class IProjectContactsSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectContactsSubtype, IContentType)


class IProjectEventsSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectEventsSubtype, IContentType)


class IProjectNewsSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectNewsSubtype, IContentType)


class IProjectLinksSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectLinksSubtype, IContentType)


class IProjectPartnersSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectPartnersSubtype, IContentType)


class IProjectMediaSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectMediaSubtype, IContentType)


class IProjectInfoSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectInfoSubtype, IContentType)


class IProjectsFolderSubtype(ISubtyped):
    """An project"""
alsoProvides(IProjectsFolderSubtype, IContentType)
