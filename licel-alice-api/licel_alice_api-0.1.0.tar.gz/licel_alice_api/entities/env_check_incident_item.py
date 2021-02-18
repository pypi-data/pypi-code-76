from enum import Enum

from .incident_item import IncidentItem
from ..utils import DictWrapper, dict_prop


class EnvCheckType(Enum):
    CUSTOM_FIRMWARE = "CUSTOM_FIRMWARE"
    DEBUG = "DEBUG"
    EMULATOR = "EMULATOR"
    HOOKS = "HOOKS"
    ROOT = "ROOT"
    WIRELESS_SECURITY = "WIRELESS_SECURITY"

    def __str__(self):
        return self.value


class EnvCheckCustomFirmware(DictWrapper):
    custom_firmware_keys: int = dict_prop()


class EnvCheckDebug(DictWrapper):
    detect_debugger_is_connected: int = dict_prop()
    detect_debugger_has_tracer_pid: int = dict_prop()


class EnvCheckEmulator(DictWrapper):
    detect_emulator: int = dict_prop()
    detect_nox: int = dict_prop()
    detect_qemu: int = dict_prop()
    detect_qemu_driver: int = dict_prop()


class EnvCheckHooks(DictWrapper):
    xposed_jar: int = dict_prop()
    xposed_apk: int = dict_prop()
    xposed_class_path: int = dict_prop()
    xposed_classes: int = dict_prop()
    xposed_stack: int = dict_prop()
    frida_libs: int = dict_prop()
    frida_hooks: int = dict_prop()
    check_for_drozer_agent_app: int = dict_prop()


class EnvCheckRoot(DictWrapper):
    detect_test_keys: int = dict_prop()
    detect_root_managment_apps: int = dict_prop()
    detect_potentially_dangerous_apps: int = dict_prop()
    detect_root_cloaking_apps: int = dict_prop()
    check_for_su_binary: int = dict_prop()
    check_for_busy_box_binary: int = dict_prop()
    check_for_dangerous_props: int = dict_prop()
    check_for_rw_paths: int = dict_prop()
    check_su_exists: int = dict_prop()
    check_for_magisk: int = dict_prop()
    check_for_magisk_manager_app: int = dict_prop()


class EnvCheckWirelessSecurity(DictWrapper):
    wireless_security_status: int = dict_prop()


class EnvCheckContentData(DictWrapper):
    env_check_type: EnvCheckType = dict_prop(wrapper=EnvCheckType)
    custom_firmware: EnvCheckCustomFirmware = dict_prop(wrapper=EnvCheckCustomFirmware)
    debug: EnvCheckDebug = dict_prop(wrapper=EnvCheckDebug)
    emulator: EnvCheckEmulator = dict_prop(wrapper=EnvCheckEmulator)
    hooks: EnvCheckHooks = dict_prop(wrapper=EnvCheckHooks)
    root: EnvCheckRoot = dict_prop(wrapper=EnvCheckRoot)
    wireless_security: EnvCheckWirelessSecurity = dict_prop(
        wrapper=EnvCheckWirelessSecurity
    )


class EnvCheckIncidentItemContent(DictWrapper):
    environment_check: EnvCheckContentData = dict_prop(wrapper=EnvCheckContentData)


class EnvCheckIncidentItem(IncidentItem):
    content: EnvCheckIncidentItemContent = dict_prop(
        wrapper=EnvCheckIncidentItemContent
    )
