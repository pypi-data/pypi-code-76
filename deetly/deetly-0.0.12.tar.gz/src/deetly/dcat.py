"""Deetly dcat.

Utility functions for validating dcat formated metadata
"""
from collections import defaultdict
from typing import Any, Dict, List

import isodate


class ValidationError:
    """ValidationError base class."""

    ERROR_OTHER = 100
    ERROR_INVALID_VALUE = 101
    ERROR_MISSING_PROPERTY = 102
    ERROR_VALIDATION_STRING_TYPE = 103
    ERROR_VALIDATION = 104
    ERROR_INVALID_PROPERTY = 105
    WARNING_MISSING_RECOMMENDED_PROPERTY = 106

    def to_string(self, code: str, fields: List) -> str:
        """Errors to string."""

        items = []
        for field in fields:
            if field.get("validator"):
                items.append(f"{field['validator'].hint}:{field['field']}")
            else:
                items.append(f"{field['field']}")
        if code == ValidationError.ERROR_MISSING_PROPERTY:
            return f"Missing mandatory props(s): {items}"
        if code == ValidationError.WARNING_MISSING_RECOMMENDED_PROPERTY:
            return f"Missing recommended props(s): {items}"
        elif code == ValidationError.ERROR_INVALID_VALUE:
            return f"Not valid: {field}"
        elif code == ValidationError.ERROR_OTHER:
            return f"Could not be validated: {items}"
        elif code == ValidationError.ERROR_VALIDATION:
            return f"Invalid type: {items}"
        elif code == ValidationError.ERROR_INVALID_PROPERTY:
            return f"Property not in DCAT schema: {items}"


class Validator(object):
    """Validator base class."""

    hint = "Not implemented validator"

    def validate(self) -> None:
        """Validate method in base class."""
        raise NotImplementedError()


class StringValidator(Validator):
    """Validator for string properties."""

    hint = "String"

    def validate(self, value: str) -> None:
        """Validate input."""
        if not isinstance(value, str):
            raise ValidationError.ERROR_VALIDATION


class IntValidator(Validator):
    """Validator for integer properties."""

    hint = "Integer"

    def validate(self, value: int) -> None:
        """Validate input."""
        if not isinstance(value, int):
            raise ValidationError.ERROR_VALIDATION


class DateValidator(Validator):
    """Validator for date or datetime properties."""

    hint = "ISO date or datetime"

    def validate(self, value: str) -> None:
        """Validate input."""
        try:
            isodate.parse_date(value)
        except Exception:
            try:
                isodate.parse_datetime(value)
            except Exception:
                raise ValidationError.ERROR_VALIDATION


class StringOrListOfStringsValidator(Validator):
    """Validator for string or list of strings properties."""

    hint = "String or list of strings"

    def validate(self, value: Any) -> None:
        """Validate input."""
        if isinstance(value, list):
            for val in value:
                if not isinstance(val, str):
                    raise ValidationError.ERROR_VALIDATION
        else:
            if not isinstance(value, str):
                raise ValidationError.ERROR_VALIDATION


class ContactValidator(Validator):
    """Validator for contact dict properties."""

    hint = "Dict"

    def validate(self, value: dict) -> None:
        """Validate input."""
        if not isinstance(value, dict):
            raise ValidationError.ERROR_VALIDATION

        if not isinstance(value["name"], str):
            raise ValidationError.ERROR_VALIDATION

        if not isinstance(value["mbox"], str):
            raise ValidationError.ERROR_VALIDATION


class DistributionValidator(Validator):
    """Validator for Distribution properties."""

    hint = "Distribution validator"

    def validate(self, value: list) -> None:
        """Validate input."""
        if not isinstance(value, list):
            raise ValidationError.ERROR_VALIDATION

        for dist in value:
            dist = Distribution(dist)
            dist.validate()


class DcatModel(object):
    """DCAT model."""

    def __init__(self, metadata: dict) -> None:
        """Constructor."""
        self.metadata = metadata
        self.mandatory = []
        self.recommended = []
        self.optional = []
        self.validators = {
            # 'accessRights':  StringValidator,
            # 'accessService':  StringValidator,
            # 'accessURL':  StringValidator,
            # 'accrualPeriodicity':  StringValidator,
            # 'availability':  StringValidator,
            "byteSize": IntValidator,
            # 'checksum':  StringValidator,
            # 'compressFormat':  StringValidator,
            # 'conformsTo':  StringValidator,
            "contactPoint": ContactValidator,
            # 'creator':  StringValidator,
            "distribution": DistributionValidator,
            # 'downloadURL':  StringValidator,
            "format": StringOrListOfStringsValidator,
            # 'hasPolicy':  StringValidator,
            # 'hasVersion':  StringValidator,
            # 'identifier':  StringValidator,
            "isReferencedBy": StringValidator,
            # 'isVersionOf':  StringValidator,
            "issued": DateValidator,
            "keyword": StringOrListOfStringsValidator,
            # 'landingPage':  StringValidator,
            "language": StringOrListOfStringsValidator,
            # 'license':  StringValidator,
            # 'mediaType':  StringValidator,
            "modified": DateValidator,
            # 'packageFormat':  StringValidator,
            "page": StringValidator,
            # 'provenance':  StringValidator,
            "publisher": ContactValidator,
            # 'qualifiedAttributionwasGeneratedBy':  StringValidator,
            # 'qualifiedRelation':  StringValidator,
            # 'relation':  StringValidator,
            # 'rights':  StringValidator,
            # 'sample':  StringValidator,
            # 'source':  StringValidator,
            # 'spatial':  StringValidator,
            "spatialResolutionInMeters": IntValidator,
            # 'status':  StringValidator,
            # 'temporal':  StringValidator,
            # 'temporalResolution':  StringValidator,
            "theme": StringOrListOfStringsValidator,
            # 'type':  StringValidator,
            # 'versionInfo':  StringValidator,
            # 'versionNotes':  StringValidator,
        }

    def get_validator(self, key: Any) -> Validator:
        """Get validator for key."""
        return self.validators.get(key, StringValidator)

    def get_properties(self) -> List:
        """Get list of all properties."""
        return [*self.mandatory, *self.recommended, *self.optional]

    def validate_content(self, errors: Dict) -> None:
        """Check if mandatory and recommended properties are included."""
        for field in self.mandatory:
            if field not in self.metadata.keys():
                errors[ValidationError.ERROR_MISSING_PROPERTY].append({"field": field})

        for field in self.recommended:
            if field not in self.metadata.keys():
                errors[ValidationError.WARNING_MISSING_RECOMMENDED_PROPERTY].append(
                    {"field": field}
                )

    def validate(self) -> List:
        """Validate."""
        errors = defaultdict(list)

        self.validate_content(errors)

        for field, value in self.metadata.items():
            if field not in self.get_properties():
                errors[ValidationError.ERROR_INVALID_PROPERTY].append({"field": field})

            try:
                validator = self.get_validator(field)
            except KeyError:
                errors[ValidationError.ERROR_INVALID_VALUE].append(
                    {"field": field, "validator": validator}
                )
            except Exception:
                errors[ValidationError.ERROR_OTHER].append(
                    {"field": field, "validator": validator}
                )

            try:
                validator.validate(value)
            except Exception:
                errors[ValidationError.ERROR_VALIDATION].append(
                    {"field": field, "validator": validator}
                )

        for key, value in errors.items():
            print(ValidationError().to_string(key, value))

        return errors


class Dataset(DcatModel):
    """DCAT Dataset."""

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        super(Dataset, self).__init__(metadata)
        self.mandatory = ["description", "title"]

        self.recommended = [
            "contactPoint",
            "distribution",
            "keyword",
            "publisher",
            "spatial",
            "temporal",
            "theme",
        ]

        self.optional = [
            "identifier",
            "sample",
            "versionNotes",
            "landingPage",
            "spatialResolutionInMeters",
            "temporalResolution",
            "qualifiedRelation",
            "accessRights",
            "accrualPeriodicity",
            "conformsTo",
            "creator",
            "hasVersion",
            "isReferencedBy",
            "isVersionOf",
            "identifier",
            "issued",
            "language",
            "modified",
            "provenance",
            "relation",
            "source",
            "type",
            "page",
            "versionInfo",
            "qualifiedAttribution" "wasGeneratedBy",
        ]


class Distribution(DcatModel):
    """DCAT Distibution."""

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        super(Distribution, self).__init__(metadata)

        self.mandatory = ["accessURL"]

        self.recommended = ["availability", "description", "format", "license"]

        self.optional = [
            "status",
            "accessService",
            "byteSize",
            "compressFormat",
            "downloadURL",
            "mediaType",
            "packageFormat",
            "spatialResolutionInMeters",
            "temporalResolution",
            "conformsTo",
            "issued",
            "language",
            "modified",
            "rights",
            "title",
            "page",
            "hasPolicy",
            "checksum",
        ]
