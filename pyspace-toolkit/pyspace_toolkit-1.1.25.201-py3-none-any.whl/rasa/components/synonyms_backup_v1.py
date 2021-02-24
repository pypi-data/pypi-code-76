import os
from typing import Any, Dict, Optional, Text

from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import ENTITIES
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.utils import write_json_to_file
import rasa.utils.io
from rasa.utils.common import raise_warning

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

try:
    from fuzzywuzzy import fuzz, process
    fuzzywuzzy_bool = True
except:
    fuzzywuzzy_bool = False

class EntitySynonymMapper(EntityExtractor):

    defaults = {
        'fuzzywuzzy_bool': False,
        'fuzzywuzzy_limit': 90,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        synonyms: Optional[Dict[Text, Any]] = None,
    ) -> None:

        super().__init__(component_config)

        self.synonyms = synonyms if synonyms else {}

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        for key, value in list(training_data.entity_synonyms.items()):
            # key : synonym values # ex: is bankasi
            # value : normalized synonym value # ex: ISCTR
            self.add_entities_if_synonyms(key, value)
            self.synonyms[xNormalizer.tr_normalize(value).lower()] = value

        for example in training_data.entity_examples:
            for entity in example.get(ENTITIES, []):
                entity_val = example.text[entity["start"] : entity["end"]]
                self.add_entities_if_synonyms(entity_val, str(entity.get("value")))
                # key : entity_val : written text # ex: elli bin
                # value : str(entity.get('value)) : processed value # ex: 50000

    def process(self, message: Message, **kwargs: Any) -> None:

        updated_entities = message.get(ENTITIES, [])[:]
        self.replace_synonyms(updated_entities)
        message.set(ENTITIES, updated_entities, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:

        if self.synonyms:
            file_name = file_name + ".json"
            entity_synonyms_file = os.path.join(model_dir, file_name)
            write_json_to_file(
                entity_synonyms_file, self.synonyms, separators=(",", ": ")
            )
            return {"file": file_name}
        else:
            return {"file": None}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["EntitySynonymMapper"] = None,
        **kwargs: Any,
    ) -> "EntitySynonymMapper":

        file_name = meta.get("file")
        if not file_name:
            synonyms = None
            return cls(meta, synonyms)

        entity_synonyms_file = os.path.join(model_dir, file_name)
        if os.path.isfile(entity_synonyms_file):
            synonyms = rasa.utils.io.read_json_file(entity_synonyms_file)
        else:
            synonyms = None
            raise_warning(
                f"Failed to load synonyms file from '{entity_synonyms_file}'.",
                docs=DOCS_URL_TRAINING_DATA_NLU + "#entity-synonyms",
            )
        return cls(meta, synonyms)

    def replace_synonyms(self, entities) -> None:
        for entity in entities:
            # need to wrap in `str` to handle e.g. entity values of type int
            # entity_value = str(entity["value"])
            entity_value = xNormalizer.tr_normalize(str(entity["value"])).lower()

            if entity_value in self.synonyms:
                entity["value"] = self.synonyms[entity_value]
                self.add_processor_name(entity)
            elif fuzzywuzzy_bool and self.component_config["fuzzywuzzy_bool"]:
                bestfuzzymatch, bestscore = process.extract(entity_value, list(self.synonyms.keys()), scorer=fuzz.ratio, limit=1)[0]
                if bestscore > self.component_config["fuzzywuzzy_limit"]: # 90
                    entity["value"] = self.synonyms[bestfuzzymatch]

    def add_entities_if_synonyms(self, entity_a, entity_b) -> None:
        if entity_b is not None:
            original = str(entity_a)
            replacement = str(entity_b)

            if original != replacement:
                original = xNormalizer.tr_normalize(original).lower()
                if original in self.synonyms and self.synonyms[original] != replacement:
                    raise_warning(
                        f"Found conflicting synonym definitions "
                        f"for {repr(original)}. Overwriting target "
                        f"{repr(self.synonyms[original])} with "
                        f"{repr(replacement)}. "
                        f"Check your training data and remove "
                        f"conflicting synonym definitions to "
                        f"prevent this from happening.",
                        docs=DOCS_URL_TRAINING_DATA_NLU + "#entity-synonyms",
                    )

                self.synonyms[original] = replacement
