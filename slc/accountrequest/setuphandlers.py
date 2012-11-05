import logging
from pkg_resources import resource_filename

from Products.ATVocabularyManager.types.vdex.vocabularyxml import IMSVDEXVocabulary

VOCAB = resource_filename('slc.accountrequest', 'data/NACE.vdex')

def importVocabularies(context):
    if context.readDataFile("is_slc.accountrequest_profile.txt") is None:
        return

    site=context.getSite()
    logger = logging.getLogger("VocabularyImporter")
    logger.info("Importing NACE Vocabulary")
    pvm = site.portal_vocabularies

    vocabname = 'NACE'
    fh = open(VOCAB, "r")
    data = fh.read()
    fh.close()
    if vocabname not in pvm.objectIds():
        vocab = IMSVDEXVocabulary(vocabname)
        pvm._setObject(vocabname, vocab, suppress_events=True)
        pvm[vocabname].importXMLBinding(data)
        logger.info("VDEX Import of %s" % vocabname)
