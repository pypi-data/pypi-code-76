from ddc.utils import stream_exec_cmd, md5


def start_build_docker_image(cwd: str):
    all_output = []
    exit_code, image_tag = __build_docker_image(all_output, cwd)
    return exit_code, "\n".join(all_output), image_tag


def __build_docker_image(all_output, cwd: str, target: str = None):
    exit_code = -1
    if target:
        build_target = "--target " + str(target)
        image_tag: str = "ddc_local/tmp:" + md5(cwd) + "_" + str(target)
    else:
        build_target = ""
        image_tag: str = "ddc_local/tmp:" + md5(cwd)

    try:
        exit_code, mix_output = stream_exec_cmd(
            ("docker build {build_target} -t " + image_tag + " " + cwd).format(
                build_target=build_target
            )
        )
        print("mix_output = %s" % str(mix_output))
        if exit_code:
            all_output.append("DDC: Build docker image")
            all_output.append(mix_output)
            raise StopIteration()

        all_output.append(mix_output)
    except StopIteration:
        pass
    return exit_code, image_tag
