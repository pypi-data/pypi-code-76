from packaging.version import Version

_main_version_components = ["major", "minor", "micro"]
_segment_version_components = ["dev", "pre", "post"]


def increment_major(version, **kwargs):
    return Version(f"{version.major + 1}.0")


def increment_minor(version, **kwargs):
    return Version(f"{version.major}.{version.minor + 1}")


def increment_micro(version, **kwargs):
    return Version(f"{version.major}.{version.minor}.{version.micro + 1}")


def perform_release(version, **kwargs):
    return Version(f"{version.base_version}")


def _get_segment(version):
    return (
        0
        if version.is_devrelease
        else 1
        if version.is_prerelease
        else 3
        if version.is_postrelease
        else 2
    )


_segments = {
    "dev": 0,
    "pre": 1,
    "post": 3,
}


def increment_segment(version, segment="dev", increment_upstream="micro", **kwargs):
    assert segment in _segment_version_components
    # eg. for "dev" equals to `version.is_devrelease`
    # eg. `segment="dev"; version=Version("0.1.dev0")` -> True
    required_segment = _segments[segment]
    has_segment = (
        0
        if version.is_devrelease
        else 1
        if version.is_prerelease
        else 3
        if version.is_postrelease
        else 2
    )
    if not (required_segment >= has_segment or increment_upstream):
        raise ValueError("Current version Segment is higher than the required one!")

    if not increment_upstream:
        # if already in the segment, update just segment
        if has_segment == required_segment:
            segment_value = getattr(version, segment)
            if isinstance(segment_value, tuple):
                segment_value = segment_value[1]
            new_segment_value = segment_value + 1
        else:
            new_segment_value = 0
        return Version(f"{version.base_version}.{segment}{new_segment_value}")

    # check if upstream is a valid piece of version
    if increment_upstream not in _main_version_components:
        raise ValueError(
            f"increment_upstream={increment_upstream} not in {_main_version_components}"
        )

    if segment != "post":
        # find out how to increment version
        if increment_upstream == "major":
            return Version(f"{version.major + 1}.0.0.{segment}0")
        elif increment_upstream == "minor":
            return Version(f"{version.major}.{version.minor + 1}.{segment}0")
        elif increment_upstream == "micro":
            return Version(
                f"{version.major}.{version.minor}.{version.micro + 1}.{segment}0"
            )
        # catch all unmanaged conditions
        raise ValueError(f"increment_upstream value {increment_upstream} is not valid.")
    else:
        raise ValueError(f"segment {segment} can not increment_upstream.")


def to_custom_version(version, custom_version, **kwargs):
    assert custom_version
    return Version(custom_version)


_version_ops = {
    "major": increment_major,
    "minor": increment_minor,
    "micro": increment_micro,
    "release": perform_release,
    "segment": increment_segment,
    "custom": to_custom_version,
}


def update_config_version(config, config_fp, element, **kwargs):
    print(f"Read config from {config_fp}")
    version = Version(config["metadata"]["version"])

    new_version = _version_ops[element](version, **kwargs)
    try:
        assert new_version > version
    except AssertionError as e:
        if element == "custom" and kwargs.get("force"):
            print("WARNING: we are reverting the version!")
        else:
            raise e

    print(f"Updating version `{version}` to `{new_version}`.")
    config["metadata"]["version"] = str(new_version)

    print("Writing back config...")
    with open(config_fp, "w") as configfile:
        config.write(configfile)
