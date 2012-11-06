from zope.site.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import TreeVocabulary
from zope.schema.vocabulary import SimpleTerm

from five import grok
from Products.ATVocabularyManager import NamedVocabulary

def _createTermTree(ttree, dict_):
    """ A helper method to convert the ATVocabularyManager TreeVocabulary into
        a dictionary that the zope.schema.vocabulary.TreeVocabulary can handle.
    """
    for key in dict_.keys():
        oldterm = dict_[key]
        title = oldterm[0]
        term = SimpleTerm(key, key, title)
        ttree[term] = TreeVocabulary.terms_factory()
        if oldterm[1] is not None:
            _createTermTree(ttree[term], oldterm[1])
    return ttree

class SectorVocabulary(object):
    """ Create a dexterity-compatible vocabulary from an
        ATVocabularyManager vocabulary.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        atv = NamedVocabulary('NACE')
        vocab = atv.getVocabularyDict(getSite())
        tree = _createTermTree(TreeVocabulary.terms_factory(), vocab)
        return TreeVocabulary(tree)

grok.global_utility(SectorVocabulary, name=u"slc.accountrequest.sector")
