from ddc.utils import stream_exec_cmd, run_if_time_has_passed


def start_black(cwd: str, lang: str):
    image_tag = "apisgarpun/pronto-black-{lang}".format(lang=lang)

    def _pull():
        stream_exec_cmd("docker pull {image_tag}".format(image_tag=image_tag))

    run_if_time_has_passed("black-" + lang, 60, _pull)
    return stream_exec_cmd(
        "docker run --rm -v {cwd}:/usr/app {image_tag}".format(
            cwd=cwd, image_tag=image_tag
        )
    )
