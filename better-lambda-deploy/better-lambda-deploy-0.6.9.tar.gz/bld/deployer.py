from .function import LambdaFunction, QueueFunction, ScheduleFunction
from .api_function import APIFunction
from jinja2 import Environment, FileSystemLoader
import os
import subprocess
import boto3
import shutil
from zipfile import ZipFile
from io import BytesIO
import botocore
import json
from .queue import Queue
import bottle
from functools import partial
import importlib
from pynamodb.models import Model
from pynamodb.exceptions import TableError


class Deployer(object):
    def __init__(
        self,
        name,
        dir,
        docker=False,
        environment="prod",
        local=False,
        subdomain=None,
        domain="alexwiss.com",
        pool_id="us-east-1_RIZE20fug",
        certificate_id="6ed4866c-16dd-4db8-81cf-fb1316227679",
    ):
        self.dir = dir
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.jinja = Environment(loader=FileSystemLoader(script_dir))
        self.project_name = name
        self.environment = environment
        self.docker = docker
        self.local = local
        self.subdomain = subdomain
        self.domain = domain
        self.pool_id = pool_id
        self.certificate_id = certificate_id
        client = boto3.client("sts")
        self.account_id = client.get_caller_identity()["Account"]
        os.environ["ENVIRONMENT"] = environment

        # Appending the current path to grab any other files.
        os.sys.path.append(os.path.abspath(self.dir))

    def _get_env_vars(self):
        # Getting environment variables.
        env_vars = []
        for name, value in os.environ.items():
            if name[0:4] == "BLD_":
                env_vars.append(
                    {
                        "name": name[4:],
                        "alpha_name": name[4:].replace("_", ""),
                        "value": value,
                        "type": "String",
                    }
                )
        return env_vars

    def _get_queues(self):
        """
        Determine queues based on classes that inherit form bld.Queue.
        """
        queues = []
        for child in Queue.__subclasses__():
            queues.append({"name": child.__name__.lower()})
        return queues

    def _get_api_subclasses(self, api_functions, start_class):
        api_classes = start_class.__subclasses__()
        # Add any subclasses
        for api in api_classes:
            inst = api()
            methods = inst.get_methods()
            if hasattr(inst, "is_lambda"):
                api_functions.append(
                    {
                        "class": api,
                        "name": api.__name__,
                        "endpoint": api.endpoint,
                        "methods": methods,
                    }
                )
            else:
                self._get_api_subclasses(api_functions, api)

    def _get_api_functions(self):
        api_functions = []
        self._get_api_subclasses(api_functions, APIFunction)
        return api_functions

    def _get_queue_functions(self):
        functions = []
        classes = QueueFunction.__subclasses__()
        for lambda_class in classes:
            if lambda_class.__name__ not in [
                "APIFunction",
                "QueueFunction",
                "ScheduleFunction",
            ]:
                functions.append(
                    {"name": lambda_class.__name__, "queue": lambda_class.queue}
                )
        return functions

    def _get_schedule_functions(self):
        functions = []
        classes = ScheduleFunction.__subclasses__()
        for lambda_class in classes:
            if lambda_class.__name__ not in [
                "APIFunction",
                "QueueFunction",
                "ScheduleFunction",
            ]:
                functions.append(
                    {"name": lambda_class.__name__, "schedule": lambda_class.schedule}
                )
        return functions

    def _get_pynamo_models(self):
        return Model.__subclasses__()

    def _install_reqs(self):
        reqs = os.path.abspath(f"{self.dir}/requirements.txt")
        subprocess.run(["pip", "install", "-r", reqs], check=True)

    def _source_files(self):
        # Running files to create subclasses.
        # TODO: Change these from hardcoded to dynamic.
        if os.path.isfile("queues.py"):
            importlib.import_module("queues")
        if os.path.isfile("function.py"):
            importlib.import_module("function")
        if os.path.isfile("api.py"):
            importlib.import_module("api")
        if os.path.isfile("model.py"):
            importlib.import_module("model")

    def _build_template(self, output_dir=None):
        # Checking custom output directory.
        output_file = f"{output_dir}/bld.yml" if output_dir else "bld.yml"

        # Installing requirements so everything is importable.
        # self._install_reqs()

        self._source_files()

        # Get all Lambda Functions.
        lambda_functions = []
        lambda_classes = LambdaFunction.__subclasses__()
        for lambda_class in lambda_classes:
            if lambda_class.__name__ not in ["APIFunction", "QueueFunction"]:
                lambda_functions.append({"name": lambda_class.__name__})

        # Get all APIFunctions.
        api_functions = self._get_api_functions()

        # Creating SAM template.
        template = self.jinja.get_template("sam.j2")

        env_vars = self._get_env_vars()
        queues = self._get_queues()

        queue_functions = self._get_queue_functions()
        schedule_functions = self._get_schedule_functions()

        rendered = template.render(
            description="Test",
            functions=lambda_functions,
            api_functions=api_functions,
            environment_variables=env_vars,
            dynamo_tables=[],
            project_name=self.project_name,
            subdomain=self.subdomain,
            domain=self.domain,
            queues=queues,
            queue_functions=queue_functions,
            schedule_functions=schedule_functions,
            pool_id=self.pool_id,
            certificate_id=self.certificate_id,
            account_id=self.account_id,
        )
        f = open(output_file, "w")
        f.write(rendered)
        f.close()

    def _local_build(self):
        build_path = os.path.abspath(f"{self.dir}/.aws-sam/build")
        if os.path.exists(build_path):
            shutil.rmtree(build_path)

        os.makedirs(build_path, exist_ok=True)

        # Install requirements.
        pip_cmd = ["pip", "install", "-r", "requirements.txt", "-t", build_path]
        subprocess.run(pip_cmd, cwd=self.dir)

        # Copy template in there.
        shutil.copyfile("bld.yml", f"{build_path}/template.yml")

        # Copying Python code to build directory.
        # TODO: Add symlinks for all Python files so live updated works.
        for (dirpath, dirnames, filenames) in os.walk(self.dir):
            files = list(filter(lambda x: x.endswith(".py"), filenames))
            break

        for f in files:
            shutil.copyfile(os.path.abspath(f"{dirpath}/{f}"), f"{build_path}/{f}")

    def _sam_build(self):
        # Run the SAM CLI to build and deploy.
        sam_build = ["sam", "build", "--debug", "--template-file", "bld.yml"]
        if self.docker:
            sam_build.append("--use-container")
        subprocess.run(sam_build, cwd=self.dir, check=True)

    def _build(self):
        if self.local:
            self._local_build()
        else:
            self._sam_build()

    def _deploy_tables(self, local):
        for model in self._get_pynamo_models():
            print(f"Deploying DynamoDB table {model.Meta.table_name}.")
            if local:
                model.Meta.host = "http://localhost:4566"

            try:
                # TODO: Should probably decide if this is how we want it to work.
                if model.exists() and local:
                    print(
                        f"Deleting existing local DynamoDB table {model.Meta.table_name}."
                    )
                    model.delete_table()

                model.create_table(wait=True)
            except TableError as e:
                if isinstance(e.cause, botocore.exceptions.EndpointConnectionError):
                    if local:
                        print(
                            "Unable to connect to LocalStack to deploy DynamoDB tables. "
                            "Have you started LocalStack on your machine ('localstack start')?"
                        )
                        exit(1)
                    else:
                        raise e
                else:
                    raise e

    def deploy(self):
        self._build_template()
        self._deploy_tables(False)

        # Creating S3 bucket for SAM.
        # TODO: Set this to create a random bucket if the name is taken or something.
        s3 = boto3.client("s3")
        s3.create_bucket(
            ACL="private", Bucket=f"{self.project_name}-bld-{self.environment}"
        )
        self._build()
        env_vars = self._get_env_vars()
        overrides = [
            f"ParameterKey={x['alpha_name']},ParameterValue={x['value']}"
            for x in env_vars
        ]
        sam_deploy = [
            "sam",
            "deploy",
            "--stack-name",
            f"{self.project_name}-bld-{self.environment}",
            "--capabilities",
            "CAPABILITY_NAMED_IAM",
            "--s3-bucket",
            f"{self.project_name}-bld-{self.environment}",
            "--template-file",
            ".aws-sam/build/template.yml",
            "--parameter-overrides",
            f"ENVIRONMENT={self.environment}",
            "--no-fail-on-empty-changeset",
        ]
        if len(overrides) > 0:
            sam_deploy.append(",".join(overrides))
        subprocess.run(sam_deploy, cwd=self.dir, check=True)

        print("Deployed successfully.")

    def _start_infra(self):
        # Saving for when I figure out how to actually run localstack
        pass

    def start_api(self, method="local"):
        """Run the API layer locally."""
        os.environ["ENVIRONMENT"] = "local"
        if method == "sam":
            self._start_api_sam()

        elif method == "local":
            self._source_files()
            self._start_infra()
            self._deploy_tables(True)
            self._start_api_local()

        else:
            raise Exception(f"Couldn't understand start API method '{method}'.")

    def _start_api_sam(self):
        self._build_template()
        self._build()

        env_vars = self._get_env_vars()
        overrides = [f"{x['alpha_name']}={x['value']}" for x in env_vars]
        overrides.append("ENVIRONMENT=sam")

        queues = self._get_queues()
        queue_functions = self._get_queue_functions()
        localstack_endpoint = "http://localhost:4566"
        iam = boto3.client("iam", endpoint_url=localstack_endpoint)
        sqs = boto3.client("sqs", endpoint_url=localstack_endpoint)
        lamb = boto3.client("lambda", endpoint_url=localstack_endpoint)

        # Deploy queues to localstack.
        for queue in queues:
            print(f"Deploying queue {queue['name']}.")
            _ = sqs.create_queue(
                QueueName=f"{self.project_name}-{queue['name']}-{self.environment}"
            )

        try:
            _ = iam.create_role(
                RoleName="lambda",
                AssumeRolePolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"Service": "lambda.amazonaws.com"},
                                "Action": "sts:AssumeRole",
                            }
                        ],
                    }
                ),
            )
        except Exception:
            print("Role exists.")

        try:
            _ = iam.put_role_policy(
                RoleName="lambda",
                PolicyName="allow",
                PolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {"Effect": "Allow", "Action": "*", "Resource": "*"},
                            {"Effect": "Allow", "Action": "logs:*", "Resource": "*"},
                            {
                                "Effect": "Allow",
                                "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
                                "Resource": ["*"],
                            },
                        ],
                    }
                ),
            )
        except Exception as e:
            print(e)
            print("Role and policy already connected.")

        # Deploy lambda functions
        # Create a ZipFile object
        zip_file = BytesIO()
        with ZipFile(zip_file, "w") as zip_obj:
            # Iterate over all the files in directory
            for folder_name, subfolders, filenames in os.walk(
                f"{self.dir}/.aws-sam/build"
            ):
                for filename in filenames:
                    # Create complete filepath of file in directory
                    file_path = os.path.join(folder_name, filename)
                    arc_path = os.path.join(
                        folder_name.replace(".aws-sam/build", ""), filename
                    )
                    # Add file to zip
                    zip_obj.write(file_path, arcname=arc_path)

        with open("test.zip", "wb") as f:
            f.write(zip_file.getbuffer())
        environment = {
            "Variables": {"ENVIRONMENT": "sam", "AWS_DEFAULT_REGION": "us-east-1"}
        }
        for function in queue_functions:
            print(f"Creating/updating function {function['name']}.")
            # Try to update the function.
            try:
                zip_file.seek(0)
                lamb.update_function_configuration(
                    FunctionName=function["name"], Environment=environment
                )
                lamb.update_function_code(
                    FunctionName=function["name"], Publish=True, ZipFile=zip_file.read()
                )

            except Exception as e:
                print(e)
                print("Function can't be updated. Creating.")
                zip_file.seek(0)
                # If it doesn't exist, create it.
                lamb.create_function(
                    FunctionName=function["name"],
                    Runtime="python3.8",
                    Handler=f"function.{function['name']}Handler",
                    Code={"ZipFile": zip_file.read()},
                    Role="arn:aws:iam::000000000000:role/lambda",
                    Environment=environment,
                )

            try:
                _ = lamb.create_event_source_mapping(
                    EventSourceArn=f"arn:aws:sqs:us-east-1:000000000000:{function['queue']}",
                    FunctionName=function["name"],
                    Enabled=True,
                    BatchSize=10,
                )
            except Exception as e:
                print(e)
                print("Event mapping already deployed.")

        sam_start = [
            "sam",
            "local",
            "start-api",
            "-d 5858",
            "--template-file",
            ".aws-sam/build/template.yml",
            "--docker-network",
            "development_private",
        ]
        if len(overrides) > 0:
            sam_start.append("--parameter-overrides")
            sam_start.append(",".join(overrides))

        subprocess.run(sam_start, cwd=self.dir, check=True)

    def _handle_response(self, func, method, *args, **kwargs):
        body = bottle.request.body.read()
        event = {"httpMethod": method, "pathParameters": {}, "body": body}
        for kwarg, val in kwargs.items():
            event["pathParameters"][kwarg] = val
        res = func(event, {})
        headers = res.get("headers", {})
        for k, v in headers.items():
            bottle.response.set_header(k, v)
        bottle.response.status = res.get("statusCode", 200)
        return res.get("body")

    def _start_api_local(self):
        api_functions = self._get_api_functions()

        @bottle.route("/test")
        def test():
            return "Hey good lookin'."

        api = importlib.import_module("api")

        for endpoint in api_functions:
            handler = getattr(api, endpoint["class"].__name__).get_handler()
            path = endpoint["endpoint"].replace("{", "<").replace("}", ">")
            bottle.route(
                path=path,
                method="OPTIONS",
                callback=partial(self._handle_response, handler, "OPTIONS"),
            )
            for method in endpoint["methods"]:
                print(f"Setting up endpoint {path} with method {method}.")
                bottle.route(
                    path=path,
                    method=method,
                    callback=partial(self._handle_response, handler, method),
                )

        bottle.run(host="localhost", port=8080)

    def invoke(self, function):
        self._build_template()
        self._build()
        subprocess.run(["sam", "local", "invoke", function], cwd=self.dir, check=True)


if __name__ == "__main__":
    deployer = Deployer("pilotproj", "../pilotproj")
    deployer.start_api()
