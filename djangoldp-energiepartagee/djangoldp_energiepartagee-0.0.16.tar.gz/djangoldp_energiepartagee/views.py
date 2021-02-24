from django.contrib.auth import get_user_model
from django.http import Http404
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template import loader
from django.conf import settings
from djangoldp.views import LDPViewSet
from djangoldp.models import Model
from datetime import date
from rest_framework import status
from djangoldp.views import NoCSRFAuthentication
import validators

from rest_framework.response import Response
from rest_framework.views import APIView


class ContributionsView(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        '''overriden dispatch method to append some custom headers'''
        response = super(ContributionsView, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.META.get('HTTP_ORIGIN')
        response["Access-Control-Allow-Methods"] = "POST"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, cache-control, pragma, user-agent"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "*/*"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response

   
    def contributionMail(self, request, specificdata):
        # Check that we get an array
        if (request.method == 'POST' and request.data and isinstance(request.data, list)):
            for urlid in request.data:
              # Check that the array entries are URLs
              if validators.url(urlid):
                # Check that the corresponding Actors exists
                model, instance = Model.resolve(urlid)
                if instance and instance.actor:
                  if instance.contributionstatus == specificdata['status_before']:
                    # Modify the contribution status
                    instance.contributionstatus = specificdata['status_after']
                    instance.calldate = date.today()
                    instance.save()

                    # Get the email templates we need
                    text_message = loader.render_to_string(
                        specificdata['email_text'],
                        {
                            'user': instance.actor.managementcontact,
                            'actor': instance.actor,
                            'contribution': instance,
                            'uri':request.build_absolute_uri('/media/'),
                        }
                    )

                    html_message = loader.render_to_string(
                        specificdata['email_html'],
                        {
                            'user': instance.actor.managementcontact,
                            'actor': instance.actor,
                            'contribution': instance,
                            'uri':request.build_absolute_uri('/media/'),
                        }
                    )
                    # Send an HTML email to the management contact of the Actor including a link to the app
                    send_mail(
                        _(specificdata['email_title']),
                        text_message,
                        settings.EMAIL_HOST_USER or "contact@energie-partagee.fr",
                        [instance.actor.managementcontact.email],
                        fail_silently=True,
                        html_message=html_message
                    )

            # Questions:
            #   public link to the HTML document ?
            #   Do we want to have it private ?

            response = Response({"content": "This is a success"}, status=status.HTTP_200_OK)
            
            return response

        return Response(status=204)
 

class ContributionsCallView(ContributionsView):
    def post(self, request):
        from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        specificdata = {
            'status_before' : CONTRIBUTION_CHOICES[0][0],
            'status_after' : CONTRIBUTION_CHOICES[1][0],
            'email_text' : 'emails/txt/subscription_call.txt',
            'email_html' : 'emails/html/subscription_call.html',
            'email_title' : 'Energie Partagée - Appel à cotisation'
        }
        return self.contributionMail(request, specificdata)


class ContributionsReminderView(ContributionsView):
    def post(self, request):
        from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        specificdata = {
            'status_before' : CONTRIBUTION_CHOICES[1][0],
            'status_after' : CONTRIBUTION_CHOICES[2][0],
            'email_text' : 'emails/txt/subscription_reminder.txt',
            'email_html' : 'emails/html/subscription_reminder.html',
            'email_title' : 'Energie Partagée - Relance d\'appel à cotisation'
        }
        return self.contributionMail(request, specificdata)     


class ContributionsVentilationView(ContributionsView):
    def post(self, request):
        from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        if request.data:
            # Check parameters
            data_expected = [
                'ventilationpercent', 
                'ventilationto',
                'ventilationdate',
                'factureventilation', 
                'contributions'
            ]

            if not all(parameter in request.data.keys() for parameter in data_expected):
                missing_params = [parameter for parameter in data_expected if parameter not in request.data.keys()]
                return Response('Invalid parameters: {} missing'.format(', '.join(missing_params)), status=400)
           
            # Check regional network
            ventilationto_urlid = request.data['ventilationto']['@id']
            if validators.url(ventilationto_urlid):
                model, instance = Model.resolve(ventilationto_urlid)
                if instance:
                    ventilationto = instance
                else:
                    return Response('Regional network does not exist in DB', status=400)

            # Check contributions 
            contribution_list = []
            for contrib_urlid in request.data['contributions']:
                if validators.url(contrib_urlid):
                    model, instance = Model.resolve(contrib_urlid)
                    if instance:
                        contribution_list.append(instance)
                    else:
                        return Response('Contribution {} does not exist in DB'.format(contrib_urlid), status=400)
 
            # Ventilate
            for contrib in contribution_list:
                contrib.ventilationpercent = request.data['ventilationpercent']
                contrib.ventilationto = ventilationto
                contrib.ventilationdate = request.data['ventilationdate']
                contrib.factureventilation = request.data['factureventilation']
                contrib.contributionstatus = CONTRIBUTION_CHOICES[4][0]
                contrib.save()

            # Send response
            response = Response({"content": "This is a success"}, status=status.HTTP_200_OK)
            
            return response

        return Response(status=204)      

class RelatedactorViewSet(LDPViewSet):
    def is_safe_create(self, user, validated_data, *args, **kwargs):
        '''
        A function which is checked before the create operation to confirm the validated data is safe to add
        returns True by default
        :return: True if the actor being posted is one which I am a member of
        '''
        if user.is_superuser:
            return True

        actor_arg = validated_data.get('actor')

        try:
            from djangoldp_energiepartagee.models import Relatedactor, Actor

            actor = Actor.objects.get(urlid=actor_arg['urlid'])

            if Relatedactor.objects.filter(user=user, actor=actor, role='admin').exists():
                return True

        except (get_user_model().DoesNotExist, KeyError):
            pass

        return False
