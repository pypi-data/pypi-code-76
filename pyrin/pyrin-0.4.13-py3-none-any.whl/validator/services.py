# -*- coding: utf-8 -*-
"""
validator services module.
"""

from pyrin.application.services import get_component
from pyrin.validator import ValidatorPackage


def register_validator(instance, **options):
    """
    registers a new validator or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a validator which is already registered.

    :param AbstractValidatorBase instance: validator to be registered.
                                           it must be an instance of
                                           AbstractValidatorBase.

    :keyword bool replace: specifies that if there is another registered
                           validator with the same domain and name, replace
                           it with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidValidatorTypeError: invalid validator type error.
    :raises DuplicatedValidatorError: duplicated validator error.
    """

    get_component(ValidatorPackage.COMPONENT_NAME).register_validator(instance, **options)


def get_domain_validators(domain):
    """
    gets all registered validators for given domain.

    it raises an error if domain does not exist.

    :param type[BaseEntity] | str domain: the domain to get its validators.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :raises ValidatorDomainNotFoundError: validator domain not found error.

    :rtype: dict[type[BaseEntity] | str, AbstractValidatorBase]
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).get_domain_validators(domain)


def get_validator(domain, name):
    """
    gets the registered validator for given domain and name.

    it returns None if no validator found for given name.

    :param type[BaseEntity] | str domain: the domain to get validator from.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param str name: validator name to get.

    :raises ValidatorDomainNotFoundError: validator domain not found error.

    :rtype: AbstractValidatorBase
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).get_validator(domain, name)


def validate_field(domain, name, value, **options):
    """
    validates the given value with given validator.

    it returns a value indicating that validator has been found.

    :param type[BaseEntity] | str domain: the domain to validate the value for.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param str name: validator name to be used for validation.
    :param object value: value to be validated.

    :keyword bool force: specifies that if there is no validator
                         with specified domain and name, it should
                         raise an error. defaults to False if not provided.

    :keyword bool nullable: determines that provided value could be None.
    :keyword bool is_list: specifies that the value must be a list of items.

    :keyword bool null_items: specifies that list items could be None.
                              it is only used if `is_list=True` is provided.

    :keyword bool inclusive_minimum: determines that values equal to
                                     accepted minimum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool inclusive_maximum: determines that values equal to
                                     accepted maximum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool allow_blank: determines that empty strings should be
                               considered valid. this argument will only
                               be considered in string validators.

    :keyword bool allow_whitespace: determines that whitespace strings should be
                                    considered valid. this argument will only
                                    be considered in string validators.

    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.
    :raises ValidationError: validation error.

    :returns: a value indicating that validator has been found.
    :rtype: bool
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_field(domain, name,
                                                                         value, **options)


def validate_dict(domain, data, **options):
    """
    validates available values of given dict.

    it uses the correct validator for each value based on its key name.

    :param type[BaseEntity] | str domain: the domain to validate the values for.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param dict data: dictionary to validate its values.

    :keyword bool lazy: specifies that all values must be validated first and
                        then a cumulative error must be raised containing a dict
                        of all keys and their corresponding error messages.
                        defaults to True if not provided.

    :keyword bool all_validators: specifies that all validators of given domain must
                                  be used for validation even if the related value is
                                  not present in data. it is useful for changing
                                  the validation behavior on insert or update
                                  operations. defaults to True if not provided.

    :keyword bool nullable: determines that provided values could be None.
    :keyword bool is_list: specifies that the value must be a list of items.

    :keyword bool null_items: specifies that list items could be None.
                              it is only used if `is_list=True` is provided.

    :keyword bool inclusive_minimum: determines that values equal to
                                     accepted minimum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool inclusive_maximum: determines that values equal to
                                     accepted maximum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool allow_blank: determines that empty strings should be
                               considered valid. this argument will only
                               be considered in string validators.

    :keyword bool allow_whitespace: determines that whitespace strings should be
                                    considered valid. this argument will only
                                    be considered in string validators.

    :raises InvalidDataForValidationError: invalid data for validation error.
    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.
    :raises ValidationError: validation error.
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_dict(domain, data,
                                                                        **options)


def validate_entity(entity, **options):
    """
    validates available values of given entity.

    it uses the correct validator for each value based on its field name.

    :param BaseEntity entity: entity to validate its values.

    :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                  which has `allow_read=False` or its name
                                                  starts with underscore `_`, should not
                                                  be included in validation. defaults to
                                                  `SECURE_TRUE` if not provided.

    :keyword bool lazy: specifies that all fields must be validated first and
                        then a cumulative error must be raised containing a dict
                        of all field names and their corresponding error messages.
                        defaults to True if not provided.

    :keyword bool all_validators: specifies that all validators of given domain must
                                  be used for validation even if the related value is
                                  not present in data. it is useful for changing
                                  the validation behavior on insert or update
                                  operations. defaults to True if not provided.

    :keyword bool nullable: determines that provided values could be None.
    :keyword bool is_list: specifies that the value must be a list of items.

    :keyword bool null_items: specifies that list items could be None.
                              it is only used if `is_list=True` is provided.

    :keyword bool inclusive_minimum: determines that values equal to
                                     accepted minimum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool inclusive_maximum: determines that values equal to
                                     accepted maximum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool allow_blank: determines that empty strings should be
                               considered valid. this argument will only
                               be considered in string validators.

    :keyword bool allow_whitespace: determines that whitespace strings should be
                                    considered valid. this argument will only
                                    be considered in string validators.

    :raises InvalidEntityForValidationError: invalid entity for validation error.
    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.
    :raises ValidationError: validation error.
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_entity(entity, **options)


def is_valid_field(domain, name, value, **options):
    """
    gets a value indicating that given field is valid.

    :param type[BaseEntity] | str domain: the domain to validate the value for.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param str name: validator name to be used for validation.
    :param object value: value to be validated.

    :keyword bool force: specifies that if there is no validator
                         with specified domain and name, it should
                         raise an error. defaults to False if not provided.

    :keyword bool nullable: determines that provided value could be None.
    :keyword bool is_list: specifies that the value must be a list of items.

    :keyword bool null_items: specifies that list items could be None.
                              it is only used if `is_list=True` is provided.

    :keyword bool inclusive_minimum: determines that values equal to
                                     accepted minimum should be considered valid.
                                     this argument will only be considered in min
                                     and range validators.

    :keyword bool inclusive_maximum: determines that values equal to
                                     accepted maximum should be considered valid.
                                     this argument will only be considered in max
                                     and range validators.

    :keyword bool allow_blank: determines that empty strings should be
                               considered valid. this argument will only
                               be considered in string validators.

    :keyword bool allow_whitespace: determines that whitespace strings should be
                                    considered valid. this argument will only
                                    be considered in string validators.

    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.

    :rtype: bool
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).is_valid_field(domain, name,
                                                                         value, **options)


def is_valid_dict(domain, data, **options):
    """
    gets a value indicating that given dict has valid values.

    it uses the correct validator for each value based on its key name.

    :param type[BaseEntity] | str domain: the domain to validate the values for.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param dict data: dictionary to validate its values.

    :keyword bool all_validators: specifies that all validators of given domain must
                                  be used for validation even if the related value is
                                  not present in data. it is useful for changing
                                  the validation behavior on insert or update
                                  operations. defaults to True if not provided.

    :keyword bool nullable: determines that provided values could be None.
    :keyword bool is_list: specifies that the value must be a list of items.

    :keyword bool null_items: specifies that list items could be None.
                              it is only used if `is_list=True` is provided.

    :keyword bool inclusive_minimum: determines that values equal to
                                     accepted minimum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool inclusive_maximum: determines that values equal to
                                     accepted maximum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool allow_blank: determines that empty strings should be
                               considered valid. this argument will only
                               be considered in string validators.

    :keyword bool allow_whitespace: determines that whitespace strings should be
                                    considered valid. this argument will only
                                    be considered in string validators.

    :raises InvalidDataForValidationError: invalid data for validation error.
    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.

    :rtype: bool
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).is_valid_dict(domain, data,
                                                                        **options)


def is_valid_entity(entity, **options):
    """
    gets a value indicating that given entity has valid values.

    it uses the correct validator for each value based on its field name.

    :param BaseEntity entity: entity to validate its values.

    :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                  which has `allow_read=False` or its name
                                                  starts with underscore `_`, should not
                                                  be included in validation. defaults to
                                                  `SECURE_TRUE` if not provided.

    :keyword bool all_validators: specifies that all validators of given domain must
                                  be used for validation even if the related value is
                                  not present in data. it is useful for changing
                                  the validation behavior on insert or update
                                  operations. defaults to True if not provided.

    :keyword bool nullable: determines that provided values could be None.
    :keyword bool is_list: specifies that the value must be a list of items.

    :keyword bool null_items: specifies that list items could be None.
                              it is only used if `is_list=True` is provided.

    :keyword bool inclusive_minimum: determines that values equal to
                                     accepted minimum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool inclusive_maximum: determines that values equal to
                                     accepted maximum should be considered valid.
                                     this argument will only be considered in min,
                                     max and range validators.

    :keyword bool allow_blank: determines that empty strings should be
                               considered valid. this argument will only
                               be considered in string validators.

    :keyword bool allow_whitespace: determines that whitespace strings should be
                                    considered valid. this argument will only
                                    be considered in string validators.

    :raises InvalidEntityForValidationError: invalid entity for validation error.
    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.

    :rtype: bool
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).is_valid_entity(entity, **options)
