from zope.interface import Interface
from zope import schema
from plone.directives import form
from plone.app.users.browser.register import IRegisterSchema
from slc.accountrequest import MessageFactory as _

class IAccountRequestInstalled(Interface):
    """Marker Interface used by as BrowserLayer
    """

class IRequestSchema(IRegisterSchema, form.Schema):
    """ This extends plone.app.users.userdataschema.IRegisterSchema and makes
        it available to dexterity, so we can create objects with this schema.
    """
    fullname = schema.TextLine(
        title=_(u'label_full_name', default=u'Full Name'),
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=False)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True)

    form.order_before(email = '*')
    form.order_before(fullname = '*')
    form.omitted('mail_me')

class IRequestFolderSchema(form.Schema):
    """ Folderish object for holding registration requests. """
