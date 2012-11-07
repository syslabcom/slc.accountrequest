from zope.component import adapter
from zope.interface import Interface, invariant, Invalid, implementer
from zope import schema
from plone.directives import form
from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from collective.dynatree.widget import DynatreeWidget
from slc.accountrequest import MessageFactory as _

class IAccountRequestInstalled(Interface):
    """Marker Interface used by as BrowserLayer
    """

class PasswordsDoNotMatch(Invalid):
    __doc__ = _(u"Passwords do not match")

@adapter(schema.interfaces.IField, IFormLayer)
@implementer(IFieldWidget)
def TreeFieldWidget(field, request):
    """ IFieldWidget factory for DynatreeWidget """
    return FieldWidget(field, DynatreeWidget(request))

class IRequestSchema(form.Schema):
    """ This extends plone.app.users.userdataschema.IRegisterSchema and makes
        it available to dexterity, so we can create objects with this schema.
    """
    fullname = schema.TextLine(
        title=_(u'label_full_name', default=u'Full Name'),
        description=_(u'help_full_name_creation',
                      default=u"Enter full name, e.g. John Smith."),
        required=True)

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True)

    organisation = schema.TextLine(
        title=_(u'label_organisation', default=u'Organisation'),
        description=_(u'help_organisation_creation',
                      default=u"Enter the name of your organisation."),
        required=True)

    sector = schema.Choice(
        vocabulary=u'slc.accountrequest.sector',
        title=_(u'label_sector', default=u'Sector'),
        description=_(u'help_sector_creation',
                      default=u"Select the relevant NACE code."),
        required=True)

    country_manager = schema.Bool(
        title=_(u'label_country_manager', default=u'Country Manager account required'),
        description=_(u'help_country_manager_creation',
                      default=u"Tick if you require a country manager account."),
        required=False)

    receive_statistics = schema.Bool(
        title=_(u'label_receive_statistics', default=u'Receive statistics'),
        description=_(u'help_receive_statistics_creation',
                      default=u"Tick if you want to receive statistics."),
        required=False)

    username = schema.ASCIILine(
        title=_(u'label_user_name', default=u'User Name'),
        description=_(u'help_user_name_creation_casesensitive',
                      default=u"Enter a user name, usually something "
                               "like 'jsmith'. "
                               "No spaces or special characters. "
                               "Usernames and passwords are case sensitive, "
                               "make sure the caps lock key is not enabled. "
                               "This is the name used to log in."))

    password = schema.Password(
        title=_(u'label_password', default=u'Password'),
        description=_(u'help_password_creation',
                      default=u'Minimum 5 characters.'))

    password_ctl = schema.Password(
        title=_(u'label_confirm_password',
                default=u'Confirm password'),
        description=_(u'help_confirm_password',
                      default=u"Re-enter the password. "
                      "Make sure the passwords are identical."))

    #form.widget(sector=TreeFieldWidget)

    @invariant
    def validatePassword(data):
        if data.password != data.password_ctl:
                raise PasswordsDoNotMatch(_(u"Password confirmation should match password."))

class IRequestFolderSchema(form.Schema):
    """ Folderish object for holding registration requests. """

class IRegistrationHandler(Interface):
    """ Marker interface for utilities that know how to register
        an account. """
    def register(self, ob):
        """ Method that does the actual registration. ``ob`` is the
            content object carrying all the information you might
            need. """
