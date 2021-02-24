APPSPEC = {
    "version": 0.0,
    "Resources": [
        {
            "TargetService": {
                "Type": "AWS::ECS::Service",
                "Properties": {
                    "TaskDefinition": "ПОМЕНЯТЬ",
                    "LoadBalancerInfo": {
                        "ContainerName": "ПОМЕНЯТЬ",
                        "ContainerPort": "ПОМЕНЯТЬ"
                    },
                    "PlatformVersion": "LATEST"
                }
            }
        }
    ]
}
