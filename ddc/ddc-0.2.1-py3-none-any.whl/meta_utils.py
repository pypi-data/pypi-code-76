import os

from ddc.utils import stream_exec_cmd, __build_path, run_if_time_has_passed


def build_bus_event(appcontent_dir):
    """
    Сборка шинных скриптов для последующего деплоя в Запускатор и запись в БД для самой меты
    """
    image_tag = "apisgarpun/pronto-meta-utils"

    def _pull():
        stream_exec_cmd("docker pull {image_tag}".format(image_tag=image_tag))

    run_if_time_has_passed("build_bus_event", 60, _pull)

    rwmeta_path = __build_path("/.rwmeta/")

    docker_args = [
        "-v {appcontent_dir}:/usr/appcontent".format(appcontent_dir=appcontent_dir),
        "-v {rwmeta_path}:/root/.rwmeta".format(rwmeta_path=rwmeta_path),
    ]

    meta_dev_token = os.environ.get("X-META-Developer-Settings")
    if meta_dev_token:
        # На серверах файлы с токенами не лежат, все делается через env
        docker_args.append(
            "-e 'X-META-Developer-Settings=" + meta_dev_token + "'"
        )

    return stream_exec_cmd(
        "docker run --rm {docker_args} {image_tag} build_bus_events".format(
            image_tag=image_tag,
            docker_args=" ".join(docker_args),
        )
    )
