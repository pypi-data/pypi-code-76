from ddc.utils import stream_exec_cmd, __build_path, run_if_time_has_passed


def build_bus_event(appcontent_dir):
    image_tag = "apisgarpun/pronto-meta-utils"

    def _pull():
        stream_exec_cmd("docker pull {image_tag}".format(image_tag=image_tag))

    run_if_time_has_passed("build_bus_event", 60, _pull)

    dev_settings_path = __build_path("/.rwmeta/developer_settings.json")
    return stream_exec_cmd(
        """
        docker run --rm \
            -v {appcontent_dir}:/usr/appcontent \
            -v {dev_settings_path}:/root/.rwmeta/developer_settings.json \
            {image_tag} \
            build_bus_events
        """.format(
            image_tag=image_tag,
            appcontent_dir=appcontent_dir,
            dev_settings_path=dev_settings_path
        )
    )


if __name__ == "__main__":
    ret, ret2 = build_bus_event(
        "/Users/arturgspb/PycharmProjects/meta-appcontent",
    )
    print("ret = %s" % str(ret))
    print("ret2 = %s" % str(ret2))
