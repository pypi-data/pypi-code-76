# -*- coding: utf-8 -*-
from plone.app.users.browser.register import RegistrationForm as BaseForm
from zope.interface import Interface
from quintagroup.formlib.captcha import Captcha
from quintagroup.formlib.captcha import CaptchaWidget
from zope.formlib import form
from plone import api
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ICCPDCaptchaSchema(Interface):
    """ """

    captcha = Captcha(
        title=u'Codice di verifica',
        description=u'Inserisci il codice di verifica che vedi.',
    )


class RegistrationForm(BaseForm):
    """
    """

    @property
    def form_fields(self):
        fields = super(RegistrationForm, self).form_fields
        fields += form.Fields(ICCPDCaptchaSchema)
        fields['captcha'].custom_widget = CaptchaWidget

        return fields

    @form.action(
        _(u'label_register', default=u'Register'),
        validator='validate_registration',
        name=u'register',
    )
    def action_join(self, action, data):
        self.handle_join_success(data)
      
        users = api.user.get_users(groupname='Site Administrators')
        portal = api.portal.get()
        portal_email = portal.getProperty('email_from_address')
        mailsubject = "Registrazione nuovo utente"
        user_name = data.get('fullname')
        user_email = data.get('email')
        for admin in users:
            admin_name = admin.getProperty('fullname')
            admin_email = admin.getProperty('email')
            try:
                mail_text="L' utente " + user_name  + " si e' iscritto al forum con l'email " + user_email  
                mail_host = api.portal.get_tool(name='MailHost')
                mail_host.send(mail_text, admin_email, portal_email, mailsubject, immediate=True)
            except:
                continue


        # XXX Return somewhere else, depending on what
        # handle_join_success returns?
        api.portal.show_message(
            message='Utente iscritto correttamente. Prima di poter accedere, controlla la tua casella email per confermare l\'attivazione.',  # noqa
            request=self.request,
        )
        came_from = self.request.form.get('came_from')
        if came_from:
            utool = api.portal.get_tool(name='portal_url')
            if utool.isURLInPortal(came_from):
                self.request.response.redirect(came_from)
                return ''
        return self.context.unrestrictedTraverse('registered')()
