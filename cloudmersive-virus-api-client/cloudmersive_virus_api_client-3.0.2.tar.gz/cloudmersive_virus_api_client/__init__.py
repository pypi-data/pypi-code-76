# coding: utf-8

# flake8: noqa

"""
    virusapi

    The Cloudmersive Virus Scan API lets you scan files and content for viruses and identify security issues with content.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

# import apis into sdk package
from cloudmersive_virus_api_client.api.scan_api import ScanApi
from cloudmersive_virus_api_client.api.scan_cloud_storage_api import ScanCloudStorageApi

# import ApiClient
from cloudmersive_virus_api_client.api_client import ApiClient
from cloudmersive_virus_api_client.configuration import Configuration
# import models into sdk package
from cloudmersive_virus_api_client.models.cloud_storage_virus_found import CloudStorageVirusFound
from cloudmersive_virus_api_client.models.cloud_storage_virus_scan_result import CloudStorageVirusScanResult
from cloudmersive_virus_api_client.models.virus_found import VirusFound
from cloudmersive_virus_api_client.models.virus_scan_advanced_result import VirusScanAdvancedResult
from cloudmersive_virus_api_client.models.virus_scan_result import VirusScanResult
from cloudmersive_virus_api_client.models.website_scan_request import WebsiteScanRequest
from cloudmersive_virus_api_client.models.website_scan_result import WebsiteScanResult
