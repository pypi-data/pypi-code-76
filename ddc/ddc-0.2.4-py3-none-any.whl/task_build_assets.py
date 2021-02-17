from ddc.task_build_docker_image import __build_docker_image
from ddc.utils import stream_exec_cmd


def start_build_assets(cwd: str, output_dir: str, docker_image_tag: str = None):
    all_output = []
    exit_code = -1
    image_tag = None
    try:
        if not docker_image_tag:
            exit_code, image_tag = __build_docker_image(all_output, cwd)
        else:
            image_tag = docker_image_tag

        docker_args = [
            "-v {output_dir}:/tmp/ddc_build_mount".format(output_dir=output_dir),
        ]

        all_output.append("Copy assets")
        exit_code, mix_output = stream_exec_cmd(
            "docker run --rm {docker_args} {image_tag} cp -R /usr/app_assets /tmp/ddc_build_mount".format(
                image_tag=image_tag, docker_args=" ".join(docker_args),
            )
        )
        all_output.append(mix_output)
    except StopIteration:
        pass
    finally:
        if not docker_image_tag and image_tag:
            stream_exec_cmd("docker image rm " + image_tag)

    return exit_code, "\n".join(all_output)
