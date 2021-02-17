import os

from ddc.task_build_docker_image import __build_docker_image
from ddc.utils import stream_exec_cmd, __build_path, get_lang_tests_dir, md5

"""
Обяателен stage building при этом названия шагов билда обязаны быть названы как build_{ИМЯ_ЯЗЫКА_ИЗ_DDC}
"""


def __discovery_build_target(cwd: str, lang: str):
    target = "build_" + str(lang)
    dockerfile_ = cwd + "/Dockerfile"
    if os.path.isfile(dockerfile_):
        with open(dockerfile_, "r") as f:
            for line in f.readlines():
                if "FROM" in line and target in line:
                    return target
    return None


def _run_test(
    cwd: str, lang: str, save_test_results: bool = False, docker_image_tag: str = None
):
    """
    Замес с exit_code и StopIteration довольно серьезный и не надо рефакторить это,
    если ты четко не понимаешь зачем это сделано
    """
    all_output = []
    exit_code = -1

    image_tag = None
    try:
        if lang == "py":
            if not os.path.exists(cwd + "/tests"):
                all_output.append("DDC: Directory /tests is not exists")
                exit_code = 1
                raise StopIteration()

            if not docker_image_tag:
                build_target = __discovery_build_target(cwd, lang)
                exit_code, image_tag = __build_docker_image(
                    all_output, cwd, build_target
                )
                if exit_code:
                    raise StopIteration()
            else:
                image_tag = docker_image_tag

            rwmeta_path = __build_path("/.rwmeta/")

            docker_args = [
                "-v {rwmeta_path}:/root/.rwmeta".format(rwmeta_path=rwmeta_path),
                "-v {cwd}:/usr/app".format(cwd=cwd),
            ]

            meta_dev_token = os.environ.get("X-META-Developer-Settings")
            if meta_dev_token:
                # На серверах файлы с токенами не лежат, все делается через env
                docker_args.append(
                    "-e 'X-META-Developer-Settings=" + meta_dev_token + "'"
                )

            pytest_args = "--reruns 2"
            if save_test_results:
                pytest_args += (
                    # " -o junit_family=xunit2 --junitxml=/usr/app/test-reports/tests.xml"
                )
            exit_code, mix_output = stream_exec_cmd(
                "docker run --rm {docker_args} {image_tag} pytest ./tests {pytest_args}".format(
                    image_tag=image_tag,
                    docker_args=" ".join(docker_args),
                    pytest_args=pytest_args,
                )
            )

            all_output.append(mix_output)
            if exit_code:
                raise StopIteration()

        elif lang == "php":
            if not os.path.exists(cwd + "/tests"):
                all_output.append("DDC: Directory /tests is not exists")
                exit_code = 1
                raise StopIteration()

            if not docker_image_tag:
                build_target = __discovery_build_target(cwd, lang)
                exit_code, image_tag = __build_docker_image(
                    all_output, cwd, build_target
                )
            else:
                image_tag = docker_image_tag

            phpunit_args = "--configuration tests/phpunit.xml"
            docker_args = []
            exit_code, mix_output = stream_exec_cmd(
                "docker run --rm {docker_args} {image_tag} ./vendor/bin/phpunit {phpunit_args} ./tests".format(
                    image_tag=image_tag,
                    docker_args=" ".join(docker_args),
                    phpunit_args=phpunit_args,
                )
            )

            all_output.append(mix_output)
            if exit_code:
                raise StopIteration()

        elif lang == "java":
            # у java особая папка
            if not os.path.exists(cwd + "/src/test"):
                all_output.append("DDC: Directory /src/test is not exists")
                exit_code = 1
                raise StopIteration()
            if not docker_image_tag:
                # на java тестим two step build для прогона тестов
                build_target = __discovery_build_target(cwd, lang)
                exit_code, image_tag = __build_docker_image(
                    all_output, cwd, build_target
                )
            else:
                image_tag = docker_image_tag

            phpunit_args = ""
            docker_args = []
            all_output.append("DDC: Start tests")
            exit_code, mix_output = stream_exec_cmd(
                "docker run --rm {docker_args} {image_tag} ./gradlew clean test".format(
                    image_tag=image_tag,
                    docker_args=" ".join(docker_args),
                    phpunit_args=phpunit_args,
                )
            )
            #  docker build --target build_java -t ddc_local/tmp:3fce479d19d3c481a4fb0f413bb42a89_build_java /Users/arturgspb/IdeaProjects/meta-jdk8
            #  docker build --target gradle_cache -t ddc_local/tmp:3fce479d19d3c481a4fb0f413bb42a89_gradle_cache /Users/arturgspb/IdeaProjects/meta-jdk8
            #  docker run --rm ddc_local/tmp:3fce479d19d3c481a4fb0f413bb42a89_build_java ./gradlew clean test

            all_output.append(mix_output)
            if exit_code:
                raise StopIteration()
        else:
            all_output.append("No test for lang: " + lang)
    except StopIteration:
        pass
    finally:
        pass
        # if not docker_image_tag and image_tag:
        #     stream_exec_cmd("docker image rm " + image_tag)
    return exit_code, "\n".join(all_output)


def start_test(
    cwd: str, lang: str, save_test_results: bool = False, docker_image_tag: str = None
):
    if lang == "auto":
        new_output = []
        exit_code = 0
        lang_tests_dir = get_lang_tests_dir(cwd)
        if not lang_tests_dir:
            return -1, "No test for any auto lang"

        for item in lang_tests_dir:
            new_output.append(
                "Test lang: " + lang + ". Dir: " + item["dir_for_run_tests"]
            )
            exit_code, lang_output = _run_test(
                item["dir_for_run_tests"],
                item["lang"],
                save_test_results,
                docker_image_tag,
            )
            new_output.append(lang_output)
            if exit_code == 0:
                new_output.append("OK")
            else:
                new_output.append("Failure...")
                break
        return exit_code, "\n".join(new_output)
    else:
        _run_test(cwd, lang, save_test_results)
