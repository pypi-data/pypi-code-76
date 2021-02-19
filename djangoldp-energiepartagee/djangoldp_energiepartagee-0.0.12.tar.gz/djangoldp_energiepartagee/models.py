from django.conf import settings
from django.db import models
from django.db.models import Max
from djangoldp.models import Model
from django.dispatch import receiver
from django.db.models import Max
from django.db.models.signals import pre_save, post_save, m2m_changed
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from djangoldp.permissions import LDPPermissions
from djangoldp.utils import is_anonymous_user
from djangoldp_energiepartagee.permissions import *
from djangoldp_energiepartagee.filters import *
from djangoldp_energiepartagee.views import RelatedactorViewSet

class Region(Model) :
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Région")
    isocode = models.CharField(max_length=6, blank=True, null=True, verbose_name="code ISO")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:region'
        
    def __str__(self):
        return self.name

class College(Model) :
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="collège")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:college'

    def __str__(self):
         return self.name

class Regionalnetwork(Model) :
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Réseau régional")
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Adresse")
    postcode = models.CharField(max_length=5, blank=True, null=True, verbose_name="Code Postal")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ville")
    colleges = models.ManyToManyField(College, blank=True, max_length=50, verbose_name="Collège")
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Code du réseau")
    logo = models.ImageField(blank=True, null=True, verbose_name="Logo")
    siren = models.CharField(max_length=20, blank=True, null=True, verbose_name="SIRET")
    usercontact = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, verbose_name="contact")
    bank = models.CharField(max_length=250, blank=True, null=True, verbose_name="Banque")
    iban = models.CharField(max_length=35, blank=True, null=True, verbose_name="IBAN")
    bic = models.CharField(max_length=15, blank=True, null=True, verbose_name="BIC")
    signature = models.ImageField(blank=True, null=True, verbose_name="Signature")
    mandat = models.CharField(max_length=250, blank=True, null=True, verbose_name="Mandat du responsable légal")
    respname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom du responsable légal")
    respfirstname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prénom du responsable légal")
    nationale = models.BooleanField(verbose_name="Réseau National", blank=True, null=True,  default=False)


    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:regionalnetwork'

    def __str__(self):
        return self.name

class Interventionzone(Model) :
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Zone d'intervention")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:interventionzone'

    def __str__(self):
        return self.name

class Legalstructure(Model) :
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Structure Juridique")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:legalstructure'

    def __str__(self):
        return self.name

class Collegeepa(Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="collège")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:collegeepa'

    def __str__(self):
         return self.name

class Paymentmethod(Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mode de paiement")

    class Meta(Model.Meta):
        permission_classes = [LDPPermissions]
        anonymous_perms = []
        authenticated_perms = ['view']
        rdf_type = 'energiepartagee:paymentmethod'

    def __str__(self):
        return self.name

class Profile(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone")
    presentation = models.TextField( blank=True, null=True, verbose_name="Présentation de l'utilisateur")
    picture =  models.CharField(blank=True, null=True, max_length=250, default="/img/default_avatar_user.svg", verbose_name="Photo de l'utilisateur")
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Adresse")
    postcode = models.CharField(max_length=5, blank=True, null=True, verbose_name="Code Postal")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ville")
    
    class Meta(Model.Meta):
        owner_field = 'user'
        authenticated_perms = ['add']
        permission_classes = [ProfilePermissions]
        rdf_type = 'energiepartagee:profile'

    def __str__(self):
        return str(self.user)

class Integrationstep(Model):
    packagestep =  models.BooleanField(blank=True, null=True, verbose_name="Colis accueil envoyé", default=False)
    adhspacestep = models.BooleanField(blank=True, null=True, verbose_name="Inscrit sur espace Adh", default=False)
    adhliststep = models.BooleanField(blank=True, null=True, verbose_name="Inscrit sur liste Adh", default=False)
    regionalliststep = models.BooleanField(blank=True, null=True, verbose_name="Inscrit sur liste régional", default=False)
    admincomment = models.TextField( blank=True, null=True, verbose_name="Commentaires de l'administrateur")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = []
        rdf_type = 'energiepartagee:integrationstep'

    def __str__(self):
        return str(self.id)

ACTORTYPE_CHOICES = [
    ('soc_citoy', 'Sociétés Citoyennes'),
    ('collectivite', 'Collectivités'),
    ('structure', 'Structures d’Accompagnement'),
    ('partenaire', 'Partenaires'),
]

CATEGORY_CHOICES = [
    ('collectivite', 'Collectivités'),
    ('porteur_dev', 'Porteurs de projet en développement'),
    ('porteur_exploit', 'Porteurs de projet en exploitation'),
    ('partenaire', 'Partenaires'),
]

class Actor (Model):
    shortname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom court de l'acteur")
    longname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom long de l'acteur")
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Adresse")
    complementaddress = models.CharField(max_length=250, blank=True, null=True, verbose_name="Complément d'adresse")
    postcode = models.CharField(max_length=5, blank=True, null=True, verbose_name="Code Postal")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ville")
    region = models.ForeignKey(Region, max_length=50, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Région", related_name='actors')
    website = models.CharField(max_length=250, blank=True, null=True, verbose_name="Site internet")
    mail = models.CharField(max_length=50, blank=True, null=True, verbose_name="Adresse mail")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone")
    iban = models.CharField(max_length=35, blank=True, null=True, verbose_name="IBAN")
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name="Lattitude")
    lng = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name="Longitude")
    status = models.BooleanField(verbose_name="Adhérent", blank=True, null=True,  default=False)
    regionalnetwork = models.ForeignKey(Regionalnetwork, blank=True, null=True, max_length=250, on_delete=models.CASCADE, verbose_name="Paiement à effectuer à")
    actortype = models.CharField(choices=ACTORTYPE_CHOICES, max_length=50, blank=True, null=True, verbose_name="Type d'acteur")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, blank=True, null=True, verbose_name="Catégorie de cotisant")
    numberpeople = models.IntegerField(blank=True, null=True, verbose_name="Nombre d'habitants")
    numberemployees = models.IntegerField(blank=True, null=True, verbose_name="Nombre d'employés")
    turnover = models.IntegerField(blank=True, null=True, verbose_name="Chiffre d'affaires")
    presentation = models.TextField(blank=True, null=True, verbose_name="Présentation/objet de la structure")
    interventionzone= models.ManyToManyField(Interventionzone, blank=True, max_length=50, verbose_name="Zone d'intervention",related_name='actors')
    logo =models.CharField(blank=True, null=True, max_length=250, default="/img/default_avatar_actor.svg", verbose_name="Logo")
    legalstructure = models.ForeignKey(Legalstructure, max_length=50, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Structure Juridique", related_name='actors')
    legalrepresentant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created', blank=True, null=True, verbose_name="Représentant légal")
    managementcontact = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,  on_delete=models.CASCADE, verbose_name="Contact Gestion")
    adhmail = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mail pour compte espace ADH")
    siren = models.CharField(max_length=20, blank=True, null=True, verbose_name="SIREN ou RNA")
    collegeepa = models.ForeignKey(Collegeepa, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Collège EPA", related_name='actors')
    college = models.ForeignKey(College, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Collège", related_name='actors')
    actorcomment = models.TextField( blank=True, null=True, verbose_name="Commentaires de l'acteur")
    signataire = models.BooleanField(blank=True, null=True, verbose_name="Signataire de la charte EP", default=False)
    adhesiondate = models.DateField(blank=True, null=True, verbose_name="Adhérent depuis")
    renewed = models.BooleanField(blank=True, null=True, verbose_name="Adhérent sur l'année en cours", default=True)
    integrationstep = models.ForeignKey(Integrationstep, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Espace administrateur", related_name="actors")
    

    @property
    def name(self):
         return "%s - %s" % ( self.shortname, self.longname )

    class Meta(Model.Meta):
        permission_classes = [ActorPermissions]
        anonymous_perms = []
        authenticated_perms = ['view', 'add']
        rdf_type = 'energiepartagee:actor'
        
    def __str__(self):
        return self.name 

CONTRIBUTION_CHOICES = [
    ('appel_a_envoye', 'Appel à envoyer'),
    ('appel_ok', 'Appel envoyé'),
    ('relance', 'Relancé'),
    ('a_ventiler', 'A ventiler'),
    ('valide', 'Validé'),
]

class Contribution(Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Acteur", related_name="contributions")
    year = models.IntegerField(blank=True, null=True, verbose_name="Année de cotisation")  
    amount = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2, verbose_name="Montant à payer")
    contributionnumber = models.IntegerField(unique=True, blank=True, null=True, verbose_name="Numéro de la cotisation")
    paymentto = models.ForeignKey(Regionalnetwork, blank=True, null=True, max_length=250, on_delete=models.CASCADE, verbose_name="Paiement à effectuer à")
    paymentmethod = models.ForeignKey(Paymentmethod, blank=True, null=True, max_length=50, on_delete=models.CASCADE, verbose_name="Moyen de paiement")
    calldate = models.DateField( blank=True, null=True, verbose_name="Date du dernier appel")
    paymentdate = models.DateField(verbose_name="Date de paiement", blank=True, null=True)
    receptdate = models.DateField(verbose_name="Date de l'envoi du reçu", blank=True, null=True)
    receivedby = models.ForeignKey(Regionalnetwork, blank=True, null=True, max_length=250, on_delete=models.CASCADE, related_name='%(class)s_requests_created', verbose_name="Paiement reçu par")
    contributionstatus =  models.CharField(choices=CONTRIBUTION_CHOICES, max_length=50, default="appel_a_envoye", blank=True, null=True, verbose_name="Etat de la cotisation")
    receptnumber = models.CharField(max_length=250, blank=True, null=True, verbose_name="Numéro de reçu")
    receptfile = models.URLField(blank=True, null=True, verbose_name="Reçu")
    callfile = models.URLField(blank=True, null=True, verbose_name="Appel à cotisations")
    ventilationpercent = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, verbose_name="pourcentage de ventilation")
    ventilationto = models.ForeignKey(Regionalnetwork, blank=True, null=True, max_length=250, on_delete=models.CASCADE,  related_name='%(class)s_ventilation', verbose_name="Bénéficiaire de la ventilation")
    ventilationdate = models.DateField(verbose_name="Date de paiement de la part ventilée", blank=True, null=True)
    factureventilation = models.CharField(max_length=25, blank=True, null=True, verbose_name="Numéro de facture de la ventilation")

    class Meta(Model.Meta):
        anonymous_perms = []
        authenticated_perms = ['view']
        permission_classes = [ContributionPermissions]
        rdf_type = 'energiepartagee:contribution'

    def __str__(self):
        return "%s - %s" % (self.actor , self.year)

ROLE_CHOICES = [
    ('admin', 'Administrateur'),
    ('membre', 'Membre'),
]

class Relatedactor(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Acteur", related_name="members")
    role  = models.CharField(choices=ROLE_CHOICES, max_length=50, blank=True, null=True, verbose_name="Rôle de l'utilisateur")

    class Meta(Model.Meta):
        permission_classes = [RelatedactorPermissions]
        view_set = RelatedactorViewSet
        rdf_type = 'energiepartagee:relatedactor'

    def __str__(self):
        return "%s - %s" % (self.user , self.actor)

    @classmethod
    def get_mine(self, user, role=None):
        if is_anonymous_user(user):
            return Relatedactor.objects.none()

        if role is None:
            return Relatedactor.objects.filter(user=user)

        return Relatedactor.objects.filter(user=user, role=role)

    @classmethod
    def get_user_actors_id(self, user, role=None):
        return self.get_mine(user=user, role=role).values_list('actor_id', flat=True)
            


@receiver(post_save, sender=Actor)
def create_actor(sender, instance, created, **kwargs):
    if created:
        if not instance.contributions or instance.contributions.exists() == False:
            amount = 0

            # Collectivity: 2c€ * Habitants - +50€ -1000€
            if instance.category == CATEGORY_CHOICES[0][0] and instance.numberpeople:
                amount = 0.02 * instance.numberpeople
                if amount < 50:
                    amount = 50
                elif amount > 1000: 
                    amount = 1000
            # Porteur_dev: 50€
            elif instance.category == CATEGORY_CHOICES[1][0]:
                amount = 50
            # Porteur_exploit: 0.5% CA +50€ -1000€
            elif instance.category == CATEGORY_CHOICES[2][0] and instance.turnover:
                amount = 0.005 * instance.turnover
                if amount < 50:
                    amount = 50
                elif amount > 1000:
                    amount = 1000
            # Partenaire: 
            #   - 1 to 4 salariés: 100€
            #   - 5 to 10 salariés: 250€
            #   - > 10 salariés: 400€
            elif instance.category == CATEGORY_CHOICES[3][0] and instance.numberemployees:
                if instance.numberemployees < 5:
                    amount = 100
                elif instance.numberemployees < 10:
                    amount = 250
                elif instance.numberemployees > 10:
                    amount = 400

            memberInstance = instance.members.create(
                role = ROLE_CHOICES[0][0],
                user = instance.managementcontact
            )
            memberInstance.save()

            contribution_max_nb = Contribution.objects.aggregate(Max('contributionnumber'))['contributionnumber__max']
            if contribution_max_nb is None:
                contribution_nb = 1
            else:
                contribution_nb = contribution_max_nb + 1

            contributionInstance = instance.contributions.create(
                year = datetime.now().year,
                amount = amount,
                paymentto = instance.regionalnetwork,
                contributionnumber = contribution_nb
            )
            contributionInstance.save()
            
            integrationstepInstance = Integrationstep(
                packagestep = False,
                adhspacestep = False,
                adhliststep = False,
                regionalliststep = False
            )
            integrationstepInstance.save()
            instance.integrationstep = integrationstepInstance
            
            instance.save()


@receiver(pre_save, sender=Contribution)
def update_status_after_payment_change(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # New contribution
        pass 
    else:
        # Detect change on payment fields
        if old_instance.receivedby == instance.receivedby or \
            old_instance.paymentmethod == instance.paymentmethod or \
            old_instance.paymentdate == instance.paymentdate :

            # Check if payment fields are filled
            if instance.receivedby is not None and \
                instance.paymentmethod is not None and \
                instance.paymentdate is not None :

                # Change status except if is already 'validé' 
                if instance.contributionstatus != CONTRIBUTION_CHOICES[4][0]:
                    instance.contributionstatus = CONTRIBUTION_CHOICES[3][0]
                    