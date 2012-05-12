import os
import logging

from Products.Five import BrowserView as FiveView

from bit.content.graphic.interfaces import IGraphical

log = logging.getLogger('bit.plone.graphic')


class FixGraphicsView(FiveView):

    def get_content(self):
        return [(x, os.path.basename(x))
                for x in self.request.get('paths') or []]

    def fix_graphics(self):
        content = self.request.get('content')
        if not content:
            return
        total = len(content)
        i = 1
        for path in content:
            try:
                obj = self.context.restrictedTraverse(path)
                
                graphical = IGraphical(obj)

                grids = graphical.graphic_ids()


                # if there is only (1/2) thing and it is thumb and endswith _thumb, switch to base
                if len(grids) < 3 and 'thumb' in grids:
                    thumb = graphical.get_raw_graphic('thumb')
                    ext = thumb.split('/').pop()
                    if 'image_' in ext:
                        base = '%simage' % thumb[:-len(ext)]
                        graphical.set_graphic('thumb', None)
                        graphical.set_graphic('base', base)

                for graphic in graphical.get_raw_list():
                    grid = graphic.split(':')[0]
                    grpath = ':'.join(graphic.split(':')[1:])
                    if grpath.startswith('/archive'):
                        new_gr = '/records%s' %grpath[8:]
                        graphical.set_graphic(grid, new_gr)

                    if grpath.startswith('archive'):
                        new_gr = '/records%s' %grpath[7:]
                        graphical.set_graphic(grid, new_gr)

                    if grpath.startswith('records/'):
                        new_gr = '/%s' %grpath
                        graphical.set_graphic(grid, new_gr)
                        
                obj.reindexObject(idxs=['graphics', 'getIcon'])
                log.warn('(%s/%s) fixing graphics for %s' % (i, total, path))
                print '(%s/%s) fixing graphics for %s' % (i, total, path)
            except:
                log.error('(%s/%s) FAIL: fixing graphics for %s' % (i, total, path))
            i += 1
