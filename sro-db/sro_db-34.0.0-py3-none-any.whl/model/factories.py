from sro_db.model.activity.models import *
from sro_db.model.artifact.models import *
from sro_db.model.core.models import *
from sro_db.model.organization.models import *
from sro_db.model.process.models import *
from sro_db.model.stakeholder.models import *
from sro_db.model.stakeholder_participation.models import *
import factory

# stakeholders_participation
class IntentedStakeholderParticipationFactory(factory.Factory):
    class Meta:
        model = IntentedStakeholderParticipation

class PerformedStakeholderParticipationFactory(factory.Factory):
    class Meta:
        model = PerformedStakeholderParticipation

class PerformedFragmentParticipationFactory(factory.Factory):
    class Meta:
        model = PerformedFragmentParticipation


# stakeholders
class PersonFactory(factory.Factory):
    class Meta:
        model = Person

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = TeamMember

class DeveloperFactory(factory.Factory):
    class Meta:
        model = Developer

class ScrumMasterFactory(factory.Factory):
    class Meta:
        model = ScrumMaster

class ProductOwnerFactory(factory.Factory):
    class Meta:
        model = ProductOwner

class ClientFactory(factory.Factory):
    class Meta:
        model = Client

# Process
class ScrumProjectFactory(factory.Factory):
    class Meta:
        model = ScrumProject

class ScrumComplexProjectFactory(factory.Factory):
    class Meta:
        model = ScrumComplexProject

class ScrumAtomicProjectFactory(factory.Factory):
    class Meta:
        model = ScrumAtomicProject

class ScrumProcessFactory(factory.Factory):
    class Meta:
        model = ScrumProcess

class ProductBacklogDefinitionFactory(factory.Factory):
    class Meta:
        model = ProductBacklogDefinition

class SprintFactory(factory.Factory):
    class Meta:
        model = Sprint

class CerimonyFactory(factory.Factory):
    class Meta:
        model = Cerimony

class PlanningMeetingFactory(factory.Factory):
    class Meta:
        model = PlanningMeeting

class DailyStandupMeetingFactory(factory.Factory):
    class Meta:
        model = DailyStandupMeeting

class ReviewMeetingFactory(factory.Factory):
    class Meta:
        model = ReviewMeeting

class RetrospectiveMeetingFactory(factory.Factory):
    class Meta:
        model = RetrospectiveMeeting

# Organization
class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization

class TeamFactory(factory.Factory):
    class Meta:
        model = Team

class ScrumTeamFactory(factory.Factory):
    class Meta:
        model = ScrumTeam

class DevelopmentTeamFactory(factory.Factory):
    class Meta:
        model = DevelopmentTeam


## Core
class ApplicationTypeFactory(factory.Factory):
    class Meta:
        model = ApplicationType

class ApplicationFactory(factory.Factory):
    class Meta:
        model = Application

class ConfigurationFactory(factory.Factory):
    class Meta:
        model = Configuration

class ApplicationReferenceFactory(factory.Factory):
    class Meta:
        model = ApplicationReference


## Artifact

class ProductBacklogFactory(factory.Factory):
    class Meta:
        model = ProductBacklog

class UserStoryFactory(factory.Factory):
    class Meta:
        model = UserStory

class EpicFactory(factory.Factory):
    class Meta:
        model = Epic

class AtomicUserStoryFactory(factory.Factory):
    class Meta:
        model = AtomicUserStory

class SprintBacklogFactory(factory.Factory):
    class Meta:
        model = SprintBacklog

class AcceptanceCriterionFactory(factory.Factory):
    class Meta:
        model = AcceptanceCriterion

class NonFunctionalAcceptanceCriterionFactory(factory.Factory):
    class Meta:
        model = NonFunctionalAcceptanceCriterion

class FunctionalAcceptanceCriterionFactory(factory.Factory):
    class Meta:
        model = FunctionalAcceptanceCriterion

### Activiy ####
class ScrumDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumDevelopmentTask

class DevelopmentTaskTypeFactory(factory.Factory):
    class Meta:
        model = DevelopmentTaskType

class PriorityFactory(factory.Factory):
    class Meta:
        model = Priority

class RiskFactory(factory.Factory):
    class Meta:
        model = Risk

class ScrumIntentedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumIntentedDevelopmentTask

class ScrumPerformedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumPerformedDevelopmentTask