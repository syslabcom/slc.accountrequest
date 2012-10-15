from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from plone.app.content.interfaces import INameFromTitle
from plone.rfc822.interfaces import IPrimaryFieldInfo
from slc.accountrequest.interfaces import IRequestSchema

class NameFromEmail(object):
    implements(INameFromTitle)
    adapts(IRequestSchema)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.email
