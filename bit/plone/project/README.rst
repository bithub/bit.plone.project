=================
bit.plone.project
=================

Let's log in

  >>> from plone.app.testing import login, setRoles
  >>> from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
  >>> setRoles(layer['portal'], TEST_USER_ID, ['Member', 'Manager'])
  >>> login(layer['portal'], TEST_USER_NAME)


ProjectsFolder Subtype
----------------------

Lets add a folder

  >>> projects_folder = layer['portal'][layer['portal'].invokeFactory('Folder', 'projects')]

Lets get the subtyper utility

  >>> from zope.component import getUtility
  >>> from p4a.subtyper import ISubtyper
  >>> subtyper = getUtility(ISubtyper)

We can change our folder to a projects folder subtype

  >>> u'bit.plone.project.ProjectsFolder' in [x.name for x in subtyper.possible_types(projects_folder)]
  True

So lets do so

  >>> subtyper.change_type(projects_folder, 'bit.plone.project.ProjectsFolder')

Let's check for the subtype marker interface

  >>> from bit.plone.project.subtypes.interfaces import IProjectsFolderSubtype
  >>> IProjectsFolderSubtype.providedBy(projects_folder)
  True

The projects folder doesnt provide the IProjectsFolder interface directly

  >>> from bit.plone.project.interfaces import IProjectsFolder
  >>> IProjectsFolder.providedBy(projects_folder)
  False

But it can be adapted to it

  >>> projects = IProjectsFolder(projects_folder)
  >>> projects
  <bit.plone.project.subtypes.projects_folder.ProjectsFolder ...>

It doesnt currently have any projects

  >>> projects.get_projects()
  []

Project Subtype
---------------

If we add a folder into our projects folder, it automagically becomes a project subtype

  >>> project1_folder = projects_folder[projects_folder.invokeFactory('Folder', 'project1')]
  >>> subtyper.existing_type(project1_folder).name
  'bit.plone.project.Project'

Project folders can be adapted to IProject

  >>> from bit.plone.project.interfaces import IProject
  >>> project1 = IProject(project1_folder)
  >>> project1
  <bit.plone.project.subtypes.projects.Project ...>

This is similar using the projects folder interface to add a project

  >>> project2 = projects.add_project('project2')
  >>> project2
  <bit.plone.project.subtypes.projects.Project ...>

Which returns the adapted project

  >>> IProject.providedBy(project2)
  True

Our projects folder now has some projects also

  >>> sorted(projects.get_projects())
  ['project1', 'project2']

And we can get the adapted project from the projects folder

  >>> project_1a = projects.get_project('project1')
  >>> project_1a
  <bit.plone.project.subtypes.projects.Project ...>

Which should equal the adapted project we already have

  >>> project_1a == project1
  True

  >>> project_1a == project2
  False

We can view the projects id

  >>> project1.get_id()
  'project1'

It doesnt have a title yet

  >>> project1.title
  ''

So let's set it

  >>> project1.title = 'Project 1'
  >>> project1.title
  'Project 1'

The project also has a UID

  >>> len(project1.uid)
  32

And a path relative to its environment

  >>> project1.path
  '/plone/projects/project1'


Special project folders
-----------------------

The project folder is currently empty

  >>> project1.context.contentIds()
  []

If we initialize the project folder

  >>> import zope.event
  >>> from Products.Archetypes.event import ObjectInitializedEvent
  >>> zope.event.notify(ObjectInitializedEvent(project1.context))

It will create some special folders for us

  >>> sorted(project1.context.contentIds())
  ['events', 'info', 'links', 'media', 'news', 'partners']

This is done automatically when adding using the IProjectsFolder.add_project function

  >>> sorted(project2.context.contentIds())
  ['events', 'info', 'links', 'media', 'news', 'partners']


Project info
------------

We can adapt the project context to IProjectContacts

  >>> from bit.plone.project.interfaces import IProjectInfo
  >>> IProjectInfo(project1.context)
  <bit.plone.project.subtypes.project_info.ProjectInfo ...>

We can get the IProjectInfo adapter from the IProject adapter also

  >>> p1_info = project1.info
  >>> p1_info
  <bit.plone.project.subtypes.project_info.ProjectInfo ...>

We havent set an email for this project yet

  >>> p1_info.email
  ''

So lets do so

  >>> p1_info.email = 'info@proj.ect'
  >>> p1_info.email
  'info@proj.ect'

The email is stored as a schema attribute of the info folder

  >>> info_folder = project1.context['info']
  >>> info_folder.Schema()['project_email'].get(info_folder)
  'info@proj.ect'

  >>> p1_info.contacts
  ['info@proj.ect']

We can add a portal user as a contact

  >>> p1_info.add_contact(TEST_USER_ID)

And it will include the user and their email if set

  >>> p1_info.contacts
  ['info@proj.ect', 'test-user <>']

These contacts are stored in the info schema

  >>> info_folder.Schema()['project_contacts'].get(info_folder)
  ('test_user_1_',)

If we add an email link, its added to the contact list 

  >>> p1_info.add_link('another-contact', 'Another contact', 'another@con.tact')

  >>> p1_info.contacts
  ['info@proj.ect', 'test-user <>', 'Another contact <another@con.tact>']

This email link is stored as "Link" with the info folder

  >>> info_folder.contentIds()
  ['another-contact']

The project url defaults to the project folders url

  >>> p1_info.url
  'http://nohost/plone/projects/project1'

You can also get a list of links associated with the project

  >>> p1_info.links
  ['http://nohost/plone/projects/project1']

We can change it

  >>> p1_info.url = 'http://somewhere.else'
  >>> p1_info.url
  'http://somewhere.else'

Both urls are now associated with the project

  >>> p1_info.links
  ['http://somewhere.else', 'http://nohost/plone/projects/project1']

Again this is stored in the info objects schema

  >>> info_folder.Schema()['project_url'].get(info_folder)
  'http://somewhere.else'

We can add another link, we need to give it an id, title and url

  >>> p1_info.add_link('another-url', 'Another URL', 'http://another.url')
  >>> p1_info.links
  ['http://somewhere.else', 'http://nohost/plone/projects/project1', 'http://another.url']  

This link is stored as "Link" with the info folder

  >>> info_folder.contentIds()
  ['another-contact', 'another-url']

Any links added to the info folder are "project links"

  >>> _yal_ = info_folder.invokeFactory('Link', 'yet-another-link')
  >>> info_folder['yet-another-link'].setRemoteUrl('http://yet.another.link')

  >>> 'http://yet.another.link' in p1_info.links
  True

The project doesnt yet have an address

  >>> p1_info.address
  ''

We can set it

  >>> p1_info.address = '777, Lucky Street,\nHappyville'
  >>> p1_info.address
  '777, Lucky Street,\nHappyville'

Again this is set on the info objects schema

  >>> info_folder.Schema()['project_address'].get(info_folder)
  '777, Lucky Street,\nHappyville'


The project doesnt yet have an phone

  >>> p1_info.phone
  ''

We can set it

  >>> p1_info.phone = '777 2323'
  >>> p1_info.phone
  '777 2323'

Again this is set on the info objects schema

  >>> info_folder.Schema()['project_phone'].get(info_folder)
  '777 2323'


Project media
-------------

We can adapt the project to IProjectMedia

  >>> from bit.plone.project.interfaces import IProjectMedia
  >>> IProjectMedia(project1.context)
  <bit.plone.project.subtypes.project_media.ProjectMedia object ...>

This is also available from the adapted project

  >>> p1_media = project1.media
  >>> p1_media
  <bit.plone.project.subtypes.project_media.ProjectMedia object ...>

TODO: media.get_latest(...)
      media.get_media(path)
      media.add_media(path, link)

maybe: media.local_media = True/False


Project Links, Events and News
------------------------------



Projects Topics
---------------


Projects Folder layouts
-----------------------


Projects Topic layouts
----------------------



Project layouts
---------------



Project info portlet
--------------------

  >>> from zope.component import getMultiAdapter
  >>> from plone.portlets.interfaces import IPortletManager, IPortletRetriever
  >>> manager = getUtility(IPortletManager, name=u"atomic.right")
  >>> retriever = getMultiAdapter((p1_info.context, manager), IPortletRetriever)

The portlet retriever for the atomic.right portletmanager is dynamic

  >>> retriever
  <bit.plone.project.browser.atomic.project_info_atoms.ProjectInfoAtomicRetriever ...>

There is a portlet called project-info

  >>> assignment = [x for x in retriever.getPortlets() if x['name'] == 'project-info'][0]['assignment']
  >>> assignment
  <Assignment at project-info>

The project path is set for the portlet assigment

  >>> assignment.path
  '/projects/project1/'

Lets get the renderer for the portlet

  >>> from plone.portlets.interfaces import IPortletRenderer
  >>> from zope.publisher.browser import BrowserView
  >>> request = layer['request']
  >>> view = BrowserView(p1_info.context, request)
  >>> renderer = getMultiAdapter((p1_info.context, request, view, manager, assignment), IPortletRenderer)
  >>> renderer
  <bit.plone.project.browser.portlets.portlet_project_info.Renderer ...>

The portlet only shows the status of the project if it is complete or occasional

  >>> renderer.status()
  ''

Lets change the status of the project

  >>> project1.status = 'complete'
  >>> renderer.status()
  'This project is not currently running, but please contact us if you would like to see it happen again'
  >>> project1.status = 'occasional'
  >>> renderer.status()
  "This project is not currently running, but drop us an email and we'll let you know next time it is"

We can access the project from the portlet

  >>> renderer.project == project1
  True

Subtype permissions
-------------------

  >>> from zope.security import checkPermission
  >>> subtypes = [x.name for x in subtyper.possible_types(projects_folder)
  ...             if checkPermission(
  ...		     x.descriptor.permission, projects_folder)]

  >>> 'bit.plone.project.Project' in subtypes
  False

  >>> 'bit.plone.project.ProjectInfo' in subtypes
  False

  >>> 'bit.plone.project.ProjectMedia' in subtypes
  False

  >>> subtypes
  [u'bit.plone.project.ProjectsFolder']





