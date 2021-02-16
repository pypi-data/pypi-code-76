import json

from madeira_tools import base
from madeira_utils import utils


class App(base.Base):

    def deploy(self):
        self._init_message()

        ############################################################
        # deploy ACM certificate for CloudFront (must be in us-east-1)
        ############################################################
        acm_certificate_arn = self.deploy_cert()

        ############################################################
        # deploy Lambda Layers for the API
        ############################################################
        layers = {
            self._app_name:
                {"path": "layers/api"},
            f"{self._app_name}_dependencies":
                {"path": f"layers/{self._app_name}_dependencies.zip"},
        }
        self._aws_lambda.deploy_layers(layers)
        layer_arns_csv = ','.join([layer_meta['arn'] for name, layer_meta in layers.items()])
        self._logger.debug(layer_arns_csv)

        ############################################################
        # deploy app infrastructure
        ############################################################
        result = self._cloudformation.create_or_update_stack(
            self._app_config['name'],
            utils.get_cf_template_for_module(__spec__),
            [
                {"ParameterKey": "ApiConfigurationSecretJson",
                 "ParameterValue": json.dumps(self._app_config)},
                {"ParameterKey": "AppName",
                 "ParameterValue": self._app_config['name']},
                {"ParameterKey": "ApiPersistenceBucketName",
                 "ParameterValue": self._app_config['api_persistence_bucket']},
                {"ParameterKey": "ApiRouterFunctionCode",
                 "ParameterValue": utils.get_file_content('functions/router.py')},
                {"ParameterKey": "ApiRouterFunctionLayerArns",
                 "ParameterValue": layer_arns_csv},
                {"ParameterKey": "CdnBucketName",
                 "ParameterValue": self._app_config['cloudfront_ui_bucket']},
                {"ParameterKey": "CdnName",
                 "ParameterValue": self._cdn_name},
                {"ParameterKey": "CertificateArn",
                 "ParameterValue": acm_certificate_arn},
                {"ParameterKey": "HostName",
                 "ParameterValue": self._app_config['hostname']}
            ],
            max_status_checks=30
        )

        if result:
            # upload the UI to the CDN bucket + update CDN cache + assure CNAME is in place
            self.update_cdn()

    def remove(self):
        self._init_message()

        # Remove DNS entry for app hostname -> CDN
        self._g_dns.delete_value(self._app_config['hostname'], 'CNAME')

        # Remove ACM certificate validation DNS entry
        cert = self._acm.get_cert_by_domain(self._app_config['hostname'])
        dns_meta = self._acm.get_cert_dns_validation_meta(cert['CertificateArn'])
        self._g_dns.delete_value(dns_meta['Name'], dns_meta['Type'])

        # Delete S3 bucket contents
        for bucket in [self._app_config['api_persistence_bucket'], self._app_config['cloudfront_ui_bucket']]:
            self._logger.info('Processing bucket: %s', bucket)

            # purge all objects without versions
            object_keys = self._s3.get_all_object_keys(bucket)
            if object_keys:
                self._logger.info('  deleting objects - please wait')
                objects_deleted = self._s3.delete_objects(bucket, object_keys)
                self._logger.info('  objects deleted: %s', objects_deleted)
            else:
                self._logger.info('  no objects (without version IDs) found')

            # purge all objects with versions + governance bypass
            object_keys = self._s3.get_all_object_versions(bucket)
            if object_keys:
                self._logger.info('  deleting object versions - please wait')
                objects_deleted = self._s3.delete_object_versions(bucket, object_keys)
                self._logger.info('  object versions deleted: %s', objects_deleted)
            else:
                self._logger.info('  no object versions found')

        # Delete CloudFormation stacks
        self._cloudformation.delete_stack(
            self._app_config['name'], disable_termination_protection=True, max_status_checks=30)

        # Delete ACM certificates
        self._acm.delete_cert_by_domain_name(self._app_config['hostname'])

        # Delete lambda layers
        for lambda_layer in self._aws_lambda.list_layers():
            if lambda_layer['LayerName'] in [self._app_name, f"{self._app_name}_dependencies"]:
                for lambda_layer_version in self._aws_lambda.list_layer_versions(lambda_layer['LayerName']):
                    self._logger.info('Deleting lambda layer: %s version: %s',
                                      lambda_layer['LayerName'], lambda_layer_version['Version'])
                    self._aws_lambda.delete_layer_version(lambda_layer['LayerArn'], lambda_layer_version['Version'])
