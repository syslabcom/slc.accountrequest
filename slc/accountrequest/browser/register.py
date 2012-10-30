import logging
import json
from five import grok
from Products.Five import BrowserView
from plone.directives import form
from plone.dexterity.utils import createContentInContainer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from slc.accountrequest.interfaces import IRequestSchema, IRequestFolderSchema
from slc.accountrequest import MessageFactory as _

grok.templatedir('.')
logger = logging.getLogger("slc.accountrequest.browser.register")

class RegistrationView(form.SchemaForm):
    grok.name('slc.accountrequest.register')
    grok.require('zope2.AccessContentsInformation')
    grok.context(IRequestFolderSchema)

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

class ReviewView(grok.View):
    """ View for approving account requests. """
    grok.name('slc.accountrequest.review')
    grok.require('cmf.ManagePortal')
    grok.context(IRequestFolderSchema)
    grok.template('review')

    def pending(self):
        pc = getToolByName(self.context, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())
        return pc(portal_type='slc.accountrequest.request',
            review_state='pending',
            path={'query': folder_path, 'depth': 1})

class ReviewActionView(grok.View):
    """ View that takes a JSON request, and approves/rejects a request. """
    grok.name('slc.accountrequest.approve')
    grok.require('cmf.ManagePortal')
    grok.context(IRequestFolderSchema)

    def render(self):
        id = self.request['id']
        action = self.request['action']

        if action not in ('approve', 'reject'):
            return json.dumps({'status': 'fail'})

        ob = self.context.get(id, None)

        self.response.setHeader("Content-Type", "application/json")
        if ob is not None:
            if action == 'reject':
                self.context.manage_delObjects(ids=[id])
                return json.dumps({'status': 'ok'})

            # action==approve, change workflow state
            wft = getToolByName(self.context, 'portal_workflow')
            try:
                wft.doActionFor(ob, 'create')
                return json.dumps({'status': 'ok'})
            except:
                logger.error('Exception while trying to approve account for' +
                             '%s <%s>',
                             ob.username,
                             ob.email)

        return json.dumps({'status': 'fail'})
