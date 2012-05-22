import base64

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class ProjectStatusVocabulary(object):
    """Vocabulary factory for ProjectStatus.
    This confuses me. I need this to work with non-english tags which seem
    to confuse zope vocabularies...
    Need to find a more elegant way of dealing with the issue ;)
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        statuses = dict(active='Active',
                        ongoing='Ongoing',
                        occasional='Occasional',
                        complete='Complete',
                        )
        return SimpleVocabulary(
            [SimpleTerm(value=k, token=base64.b64encode(k), title=v)
             for k, v in statuses.items()])

ProjectStatusVocabularyFactory = ProjectStatusVocabulary()
