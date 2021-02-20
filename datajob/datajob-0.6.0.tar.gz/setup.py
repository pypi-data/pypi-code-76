# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajob', 'datajob.glue', 'datajob.package', 'datajob.stepfunctions']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk.aws-glue==1.87.1',
 'aws-cdk.aws-s3-deployment==1.87.1',
 'aws-cdk.cloudformation-include==1.87.1',
 'aws-cdk.core==1.87.1',
 'aws-empty-bucket>=2.4.0,<3.0.0',
 'contextvars>=2.4,<3.0',
 'dephell>=0.8.3,<0.9.0',
 'stepfunctions>=1.1.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['datajob = datajob.datajob:run']}

setup_kwargs = {
    'name': 'datajob',
    'version': '0.6.0',
    'description': 'Build and deploy a serverless data pipeline with no effort on AWS.',
    'long_description': '# Datajob\n\n#### Build and deploy a serverless data pipeline with no effort on AWS.\n\n- Deploy your code to a glue job.\n- Package your project and make it available for your glue jobs.\n- Orchestrate your pipeline using stepfunctions as simple as `task1 >> [task2,task3] >> task4`\n\n> The main dependencies are [AWS CDK](https://github.com/aws/aws-cdk) and [Step Functions SDK for data science](https://github.com/aws/aws-step-functions-data-science-sdk-python) <br/>\n> Ideas to be implemented can be found [below](#ideas) <br/>\n> [Feedback](https://github.com/vincentclaes/datajob/discussions) is much appreciated!\n\n\n# Installation\n\n Datajob can be installed using pip. <br/>\n Beware that we depend on [aws cdk cli](https://github.com/aws/aws-cdk)!\n\n    pip install datajob\n    npm install -g aws-cdk@1.87.1 # latest version of datajob depends this version\n\n# Quickstart\n\n## Configure the pipeline\n**We have 3 scripts that we want to orchestrate sequentially and in parallel on AWS using Glue and Step Functions**.\n\n    from datajob.datajob_stack import DataJobStack\n    from datajob.glue.glue_job import GlueJob\n    from datajob.stepfunctions.stepfunctions_workflow import StepfunctionsWorkflow\n\n\n    # the datajob_stack is the instance that will result in a cloudformation stack.\n    # we inject the datajob_stack object through all the resources that we want to add.\n    with DataJobStack(stack_name="data-pipeline-simple") as datajob_stack:\n\n        # here we define 3 glue jobs with the datajob_stack object,\n        # a name and the relative path to the source code.\n        task1 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task1",\n            job_path="data_pipeline_simple/task1.py",\n        )\n        task2 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task2",\n            job_path="data_pipeline_simple/task2.py",\n        )\n        task3 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task3",\n            job_path="data_pipeline_simple/task3.py",\n        )\n\n        # we instantiate a step functions workflow and add the sources\n        # we want to orchestrate. We got the orchestration idea from\n        # airflow where we use a list to run tasks in parallel\n        # and we use bit operator \'>>\' to chain the tasks in our workflow.\n        with StepfunctionsWorkflow(\n            datajob_stack=datajob_stack, name="data-pipeline-simple"\n        ) as sfn:\n            [task1, task2] >> task3\n\nThe definition of our pipeline can be found in `examples/data_pipeline_simple/datajob_stack.py`, and here below:\n\n\n## Deploy\n\nSet the aws account number and the profile that contains your aws credentials (`~/.aws/credentials`) as environment variables:\n\n    export AWS_PROFILE=my-profile\n    export AWS_DEFAULT_REGION=your-region # e.g. eu-west-1\n\nPoint to the configuration of the pipeline using `--config` and deploy\n\n    cd examples/data_pipeline_simple\n    datajob deploy --config datajob_stack.py\n\n# Run\nAfter running the `deploy` command, the code of the 3 tasks are deployed to a glue job and the glue jobs are orchestrated using step functions.\nGo to the AWS console to the step functions service, look for `data-pipeline-simple` and click on "Start execution"\n\n![DataPipelineSimple](assets/data-pipeline-simple.png)\n\nFollow up on the progress.\n\n# Destroy\n\nOnce the pipeline is finished you can pull down the pipeline by using the command:\n\n    datajob destroy --config datajob_stack.py\n\nAs simple as that!\n\n> Note: When using datajob cli to deploy a pipeline, we shell out to aws cdk.\n> You can circumvent shelling out to aws cdk by running `cdk` explicitly.\n> datajob cli prints out the commands it uses in the back to build the pipeline.\n> If you want, you can use those.\n\n# Ideas\n\nAny suggestions can be shared by starting a [discussion](https://github.com/vincentclaes/datajob/discussions)\n\nThese are the ideas, we find interesting to implement;\n\n- trigger a pipeline using the cli; `datajob run --pipeline my-simple-pipeline`\n- implement a data bucket, that\'s used for your pipeline.\n- add a time based trigger to the step functions workflow.\n- add an s3 event trigger to the step functions workflow.\n- add a lambda that copies data from one s3 location to another.\n- version your data pipeline.\n- implement sagemaker services\n    - processing jobs\n    - hyperparameter tuning jobs\n    - training jobs\n    - create sagemaker model\n    - create sagemaker endpoint\n    - expose sagemaker endpoint to the internet by levering lambda + api gateway\n\n- create a serverless UI that follows up on the different pipelines deployed on possibly different AWS accounts using Datajob\n',
    'author': 'Vincent Claes',
    'author_email': 'vincent.v.claes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vincentclaes/datajob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
