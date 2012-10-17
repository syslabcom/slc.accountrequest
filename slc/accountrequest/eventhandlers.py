import logging
from zope.i18n import translate
from zope.i18nmessageid import Message
from Products.CMFCore.utils import getToolByName
from slc.accountrequest import MessageFactory as _

logger = logging.getLogger("slc.accountrequest.eventhandlers")

MAIL_NOTIFICATION_MESSAGE = _(
    u"mail_notification_message",
    default=u"Your account was created with the following details:\n\n"
             "User Name: ${username}\n"
             "Password: ${password}\n")

def createAccount(obj, event):
    # TODO create account here
    # Look up adapters, call them to do actual registration
    if event.new_state.id == 'created':
        # Transitioning from pending to created
        pass

def notifyAccountCreated(obj, event):
    if event.new_state.id == 'created':
        # Send an email to let the user know his account was approved
        mail_host = getToolByName(obj, 'MailHost')
        portal_url = getToolByName(obj, 'portal_url')
        portal = portal_url.getPortalObject()
        sender = portal.getProperty('email_from_address')
        if not sender:
            return

        subject = translate(u"Login details for ${username}",
            mapping={'username': obj.username},
            context=obj.REQUEST)
        message = translate(Message(
                MAIL_NOTIFICATION_MESSAGE,
                mapping={'username': obj.username,
                         'password': obj.password}),
                context=obj.REQUEST)
        try:
            mail_host.send(message, obj.email, sender, subject, charset='utf-8')
        except SMTPException:
            logger.error('SMTP exception while trying to send an ' +
                         'email from %s to %s',
                         sender,
                         obj.email)
