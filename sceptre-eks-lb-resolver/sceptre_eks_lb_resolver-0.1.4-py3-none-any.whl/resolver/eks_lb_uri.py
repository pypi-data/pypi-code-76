from argparse import ArgumentParser
from shlex import split as args_split

from sceptre.resolvers import Resolver

from kubernetes import client
from kubernetes import config


__author__ = "Gustavo Pantuza <gustavopantuza@gmail.com>"


class EksLbDns(Resolver):
    """
    Resolver for getting Load Balancer DNS on a Kubernetes resource of type
    Service LoadBalancer

    :param argument: -n | --namespace The namespace where the service lives in
    :type argument: str

    :param argument: -s | --service-name The service name. It must be of type LoadBalancer
    :type argument: str

    Examples Yaml usage:
      LBArn: !eks_lb_uri --namespace {{ var.namespace }} --service-name {{ var.service }}
      LBArn: !eks_lb_uri -n {{ var.namespace }} -s {{ var.service }}
      LBArn: !eks_lb_uri -s {{ var.service }}  # Assumes default namespace
      LBArn: !eks_lb_uri -s "my_api_service_name"
      LBArn: !eks_lb_uri -n backend -s data_api

    Notes:
        Be aware that the shell which sceptre will be called MUST be
        authenticated on AWS and your kubeconfig properly updated to point to
        your AWS EKS remote cluster.

        You can refer to the following links for either AWS and Kubernetes
        authentication:

          . https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html
          . https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
    """

    # Service type to be verified on k8s services
    # https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer
    SERVICE_TYPE = "LoadBalancer"

    def __init__(self, *args, **kwargs):
        """ Configures the class to be able to properly communicate with
        kubernetes remote cluster
        """

        super(EksLbDns, self).__init__(*args, **kwargs)
        self.load_args()

        config.load_kube_config()
        self.k8s = client.CoreV1Api()

    def load_args(self):
        """ Loads command line arguments from shell and turn it into class member """

        parser = ArgumentParser()

        parser.add_argument("-n", "--namespace", type=str, default="default")
        parser.add_argument("-s", "--service-name", required=True, type=str)
        args = parser.parse_args(args_split(self.argument))

        self.namespace = args.namespace
        self.service = args.service_name

    def resolve(self):
        """ Is called by Sceptre in order to retrieve k8s resource.

            This method uses kubernetes client to connect on the remote cluster
            and retrieve data of the given service name from inside the given
            namespace.

            Example Yaml usage:
              LBArn: !eks_lb_uri --namespace {{ var.namespace }} --service-name {{ var.service }}
        """

        services = self.k8s.list_service_for_all_namespaces_with_http_info()

        service = None
        for srv in services[0].items:

            # Check if the service is the one we are looking for
            if srv.metadata.namespace == self.namespace and srv.metadata.name == self.service:
                service = srv

        if not service:
            raise ValueError("Could not find Service {0}".format(self.service))

        if service.spec.type != self.SERVICE_TYPE:
            raise ValueError("Only Services of type Load Balancer are accepted")

        try:
            # Returns the Load Balancer DNS URI
            return service.status.load_balancer.ingress[0].hostname

        except AttributeError:
            raise
        except Exception as e:
            raise Exception("Could not get LB DNS. Error: {0}".format(str(e)))
