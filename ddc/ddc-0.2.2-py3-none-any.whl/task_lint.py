from ddc.utils import stream_exec_cmd, run_if_time_has_passed, get_exists_langs


def _run_lint(cwd, lang):
    image_tag = "apisgarpun/pronto-linter-{lang}".format(lang=lang)

    def _pull():
        stream_exec_cmd("docker pull {image_tag}".format(image_tag=image_tag))

    run_if_time_has_passed("lint-" + lang, 60, _pull)
    exit_code, max_output = stream_exec_cmd(
        "docker run --rm -v {cwd}:/usr/app {image_tag}".format(
            cwd=cwd, image_tag=image_tag
        )
    )
    if (
        image_tag + ":latest not found" in max_output
        or image_tag + ", repository does not exist" in max_output
    ):
        exit_code = 0
        max_output = "Skip check lang. We not found pronto linter plugin. lang: " + lang

    new_output = []
    cwd_prefix = cwd if cwd.endswith("/") else cwd + "/"
    for line in max_output.split("\n"):
        if str(line).startswith("./"):
            line = cwd_prefix + line[2:]
        new_output.append(line)
    return exit_code, "\n".join(new_output)


def start_lint(cwd, lang):
    if lang == "auto":
        new_output = []
        exit_code = 0
        for lang in get_exists_langs(cwd):
            new_output.append("Check lang: " + lang)
            exit_code, lang_output = _run_lint(cwd, lang)
            new_output.append(lang_output)
            if exit_code == 0:
                new_output.append("OK")
            else:
                new_output.append("Failure...")
                break
        return exit_code, "\n".join(new_output)
    return _run_lint(cwd, lang)
