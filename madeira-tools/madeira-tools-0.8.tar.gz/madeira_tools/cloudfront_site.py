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
        # deploy app infrastructure
        ############################################################
        result = self._cloudformation.create_or_update_stack(
            self._app_config['name'],
            utils.get_cf_template_for_module(__spec__),
            [
                {"ParameterKey": "AppName",
                 "ParameterValue": self._app_config['name']},
                {"ParameterKey": "CdnBucketName",
                 "ParameterValue": self._app_config['cloudfront_ui_bucket']},
                {"ParameterKey": "CdnName",
                 "ParameterValue": self._cdn_name},
                {"ParameterKey": "CertificateArn",
                 "ParameterValue": acm_certificate_arn},
                {"ParameterKey": "HostName",
                 "ParameterValue": self._app_config['hostname']},
            ],
            max_status_checks=30
        )

        if result:
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
        for bucket in [self._app_config['cloudfront_ui_bucket']]:
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
