# -*- coding: utf-8 -*-
from ddb.feature.schema import FeatureSchema
from marshmallow import fields, Schema


class ExtraServiceSchema(Schema):
    """
    Extra Service
    """
    https = fields.Bool(required=False, allow_none=True, default=None)
    url = fields.String(required=True, allow_none=False, default=None)
    domain = fields.String(required=True, allow_none=True, default=None)
    rule = fields.String(required=False, allow_none=True, default=None)
    redirect_to_https = fields.Boolean(required=False, allow_none=True, default=None)
    path_prefix = fields.String(required=False, allow_none=True, default=None)
    redirect_to_path_prefix = fields.Boolean(required=False, allow_none=True, default=None)


class TraefikSchema(FeatureSchema):
    """
    Traefik feature schema.
    """
    certs_directory = fields.String(required=False, allow_none=True, default=None)
    config_directory = fields.String(required=False, allow_none=True, default=None)
    mapped_certs_directory = fields.String(required=True, default="/certs")
    ssl_config_template = fields.String(required=True, default="""
# This configuration file has been automatically generated by ddb
[[tls.certificates]]
  certFile = "{{_local.certFile}}"
  keyFile = "{{_local.keyFile}}"

""".lstrip())
    extra_services = fields.Dict(fields.String(), fields.Nested(ExtraServiceSchema()), default={})
    extra_services_config_template = fields.String(required=True, default="""
# This configuration file has been automatically generated by ddb
[http.routers]
{%- if _local.https is none or _local.https is sameas false %}
  [http.routers.extra-service-{{_local.id}}]
    rule = "{{_local.rule}}"{% if not _local.redirect_to_https and _local.path_prefix %} && "PathPrefix(`{{_local.path_prefix}}{regex:$$|/.*}`)"{% endif %}
    entrypoints = ["http"]
    service = "extra-service-{{_local.id}}"
{%- if _local.redirect_to_https %}
    middlewares = ["extra-service-{{_local.id}}-redirect-to-https"]
{%- elif _local.path_prefix %}
    middlewares = ["extra-service-{{_local.id}}-stripprefix"]
{%- endif %}
{%- endif %}
{%- if _local.https is none or _local.https is sameas true %}
  [http.routers.extra-service-{{_local.id}}-tls]
    rule = "{{_local.rule}}{% if _local.path_prefix %} && PathPrefix(`{{_local.path_prefix}}{regex:$$|/.*}`){% endif %}"
    entrypoints = ["https"]
    tls = true
    service = "extra-service-{{_local.id}}"
{%- if _local.path_prefix %}
    middlewares = ["extra-service-{{_local.id}}-stripprefix"]
{%- endif %}
{%- if _local.certresolver is defined %}
    [http.routers.extra-service-{{_local.service}}-tls.tls]
      certResolver = "{{_local.certresolver}}"
{%- endif %}
{%- endif %}
{%- if _local.redirect_to_path_prefix %}
{%- if _local.https is none and not _local.redirect_to_https or _local.https is sameas false %}
  [http.routers.extra-service-{{_local.id}}-redirect-to-path-prefix]
    rule = "{{_local.rule}}"
    entrypoints = ["http"]
    service = "extra-service-{{_local.id}}"
    middlewares = ["extra-service-{{_local.id}}-redirect-to-path-prefix"]
{%- endif %}
{%- if _local.https is none or _local.https is sameas true %}
  [http.routers.extra-service-{{_local.id}}-redirect-to-path-prefix-tls]
    rule = "{{_local.rule}}"
    entrypoints = ["https"]
    tls = true
    service = "extra-service-{{_local.id}}"
    middlewares = ["extra-service-{{_local.id}}-redirect-to-path-prefix"]
{%- if _local.certresolver is defined %}
    [http.routers.extra-service-{{_local.service}}-tls.tls]
      certResolver = "{{_local.certresolver}}"
{%- endif %}
{%- endif %}
{%- endif %}

{%- if _local.redirect_to_https or _local.path_prefix  %}

[http.middlewares]
{%- if _local.redirect_to_https %}
  [http.middlewares.extra-service-{{_local.id}}-redirect-to-https.redirectScheme]
    scheme = "https"
{%- endif %}
{%- if _local.path_prefix %}
  [http.middlewares.extra-service-{{_local.id}}-stripprefix.stripPrefix]
    prefixes = "{{_local.path_prefix}}"
{%- endif %}
{%- if _local.redirect_to_path_prefix %}
  [http.middlewares.extra-service-{{_local.id}}-redirect-to-path-prefix.redirectregex]
    regex = "^.*$"
    replacement = "{{_local.path_prefix}}"
{%- endif %}
{%- endif %}

[http.services]
  [http.services.extra-service-{{_local.id}}]
    [http.services.extra-service-{{_local.id}}.loadBalancer]
      [[http.services.extra-service-{{_local.id}}.loadBalancer.servers]]
        url = "{{_local.url}}"

""".lstrip())
