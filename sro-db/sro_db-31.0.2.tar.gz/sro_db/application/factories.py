from sro_db.application.activity.application import *
from sro_db.application.artifact.application import *
from sro_db.application.core.application import *
from sro_db.application.organization.application import *
from sro_db.application.process.application import *
from sro_db.application.stakeholder.application import *
from sro_db.application.stakeholder_participation.application import *
import factory

#stakeholder participation
class IntentedStakeholderParticipationFactory(factory.Factory):
    class Meta:
        model = ApplicationIntentedStakeholderParticipation

class PerformedStakeholderParticipationFactory(factory.Factory):
    class Meta:
        model = ApplicationPerformedStakeholderParticipation

class PerformedFragmentParticipationFactory(factory.Factory):
    class Meta:
        model = ApplicationPerformedFragmentParticipation

# stakeholders
class PersonFactory(factory.Factory):
    class Meta:
        model = ApplicationPerson

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = ApplicationTeamMember

class DeveloperFactory(factory.Factory):
    class Meta:
        model = ApplicationDeveloper

class ScrumMasterFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumMaster

# Process
class ScrumProjectFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumProject

class ScrumComplexProjectFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumComplexProject

class ScrumAtomicProjectFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumAtomicProject

class ScrumProcessFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumProcess

class ProductBacklogDefinitionFactory(factory.Factory):
    class Meta:
        model = ApplicationProductBacklogDefinition

class SprintFactory(factory.Factory):
    class Meta:
        model = ApplicationSprint

# Organization
class OrganizationFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganization

class TeamFactory(factory.Factory):
    class Meta:
        model = ApplicationTeam

class ScrumTeamFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumTeam

class DevelopmentTeamFactory(factory.Factory):
    class Meta:
        model = ApplicationDevelopmentTeam


## Core
class ApplicationTypeFactory(factory.Factory):
    class Meta:
        model = ApplicationApplicationType

class ApplicationFactory(factory.Factory):
    class Meta:
        model = ApplicationApplication

class ConfigurationFactory(factory.Factory):
    class Meta:
        model = ApplicationConfiguration

class ApplicationReferenceFactory(factory.Factory):
    class Meta:
        model = ApplicationApplicationReference


## Artifact

class ProductBacklogFactory(factory.Factory):
    class Meta:
        model = ApplicationProductBacklog

class UserStoryFactory(factory.Factory):
    class Meta:
        model = ApplicationUserStory

class EpicFactory(factory.Factory):
    class Meta:
        model = ApplicationEpic

class AtomicUserStoryFactory(factory.Factory):
    class Meta:
        model = ApplicationAtomicUserStory

class SprintBacklogFactory(factory.Factory):
    class Meta:
        model = ApplicationSprintBacklog

### Activiy ####
class ScrumDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumDevelopmentTask

class DevelopmentTaskTypeFactory(factory.Factory):
    class Meta:
        model = ApplicationDevelopmentTaskType

class PriorityFactory(factory.Factory):
    class Meta:
        model = ApplicationPriority

class RiskFactory(factory.Factory):
    class Meta:
        model = ApplicationRisk

class ScrumIntentedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumIntentedDevelopmentTask

class ScrumPerformedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ApplicationScrumPerformedDevelopmentTask