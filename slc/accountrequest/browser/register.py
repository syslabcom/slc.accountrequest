from five import grok
from Products.Five import BrowserView
from plone.directives import form
from plone.dexterity.utils import createContentInContainer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import IFolderish
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from slc.accountrequest.interfaces import IRequestSchema
from slc.accountrequest import MessageFactory as _

grok.templatedir('.')

class RegistrationView(form.SchemaForm):
    grok.name('slc.accountrequest.register')
    grok.require('zope2.View')
    grok.context(IFolderish)

    schema = IRequestSchema
    ignoreContext = True

    label = _(u"Enter your account details")
    description = _(u"We will contact you once your account has been created.")

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(RegistrationView, self).update()

    @button.buttonAndHandler(_(u'Send request'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        createContentInContainer(self.context,
            'slc.accountrequest.request', **data)

        # Redirect back to the front page with a status message
        IStatusMessage(self.request).addStatusMessage(
                _(u"Thank you for your request. We will contact you shortly"),
                "info"
            )
        portal_url = self.context.restrictedTraverse(
            '@@plone_portal_state').portal_url()
        self.request.response.redirect(portal_url)

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        portal_url = self.context.restrictedTraverse(
            '@@plone_portal_state').portal_url()
        self.request.response.redirect(portal_url)

class ApprovalView(grok.View):
    """ View for approving account requests. """
    grok.name('slc.accountrequest.approve')
    grok.require('cmf.ManagePortal')
    grok.context(IRequestSchema)
    grok.template('approve')
