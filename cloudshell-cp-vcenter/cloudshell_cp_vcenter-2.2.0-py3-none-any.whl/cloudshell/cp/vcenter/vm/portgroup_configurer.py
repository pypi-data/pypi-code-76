# -*- coding: utf-8 -*-

from threading import Lock

from pyVmomi import vim

from cloudshell.cp.vcenter.network.dvswitch.creator import DvPortGroupCreator
from cloudshell.cp.vcenter.network.network_specifications import network_is_portgroup


class VNicDeviceMapper(object):
    def __init__(self, vnic, requested_vnic, network, connect, mac):
        self.vnic = vnic
        self.requested_vnic = requested_vnic
        self.network = network
        self.connect = connect
        self.vnic_mac = mac


class VirtualMachinePortGroupConfigurer(object):
    def __init__(
        self,
        pyvmomi_service,
        synchronous_task_waiter,
        vnic_to_network_mapper,
        vnic_service,
        name_gen,
    ):
        """
        :param pyvmomi_service: vCenter API wrapper
        :param synchronous_task_waiter: Task Performer Service
        :type synchronous_task_waiter: cloudshell.cp.vcenter.common.vcenter.task_waiter.SynchronousTaskWaiter
        :param vnic_to_network_mapper: VnicToNetworkMapper
        :param vnic_service: VNicService
        :type vnic_service: cloudshell.cp.vcenter.network.vnic.vnic_service.VNicService
        :return:
        """
        self.pyvmomi_service = pyvmomi_service
        self.synchronous_task_waiter = synchronous_task_waiter
        self.vnic_to_network_mapper = vnic_to_network_mapper
        self.vnic_service = vnic_service
        self.network_name_gen = name_gen
        self._lock = Lock()

    def connect_vnic_to_networks(
        self, vm, mapping, default_network, reserved_networks, logger
    ):
        try:

            vnic_mapping = self.vnic_service.map_vnics(vm)
            vnic_to_network_mapping = self.vnic_to_network_mapper.map_request_to_vnics(
                mapping, vnic_mapping, vm.network, default_network, reserved_networks
            )

            update_mapping = []
            for vnic_name, map in list(vnic_to_network_mapping.items()):
                vnic = vnic_mapping[vnic_name]
                requseted_vnic = map[1]
                network = map[0]
                update_mapping.append(
                    VNicDeviceMapper(
                        vnic, requseted_vnic, network, True, vnic.macAddress
                    )
                )

            self.update_vnic_by_mapping(vm, update_mapping, logger)
            return update_mapping
        except Exception as e:
            # If we fail to connect to a vm, make sure we clear the mapping and delete the network if necessary
            #
            # Example: we have a VM with no nics (ethernet adapters).
            # We have created a vlan for this VM, but were unable to connect to any nic.
            # We dispose of the VLAN now, rolling back the network
            # This way we don't have to deal with disposing of the vlan later when no object references the vlan
            # since it wasnt mapped to any nic
            self.erase_network_by_mapping(
                [request.network for request in mapping], reserved_networks, logger
            )
            logger.exception("Failed to connect VM: {}".format(vm.name))
            raise ValueError('VM: {0} failed with: "{1}"'.format(vm.name, e))

    def erase_network_by_mapping(self, networks, reserved_networks, logger):
        nets = dict()
        self._lock.acquire()
        try:
            for net in networks:
                try:
                    nets[net.name] = net
                except:
                    continue

                for network in list(nets.values()):
                    try:
                        if (
                            self.network_name_gen.is_generated_name(network.name)
                            and (
                                not reserved_networks
                                or network.name not in reserved_networks
                            )
                            and not network.vm
                        ):

                            task = self.destroy_port_group_task(network)
                            if task:
                                self.synchronous_task_waiter.wait_for_task(
                                    task=task,
                                    logger=logger,
                                    action_name="Erase dv Port Group",
                                )
                    except Exception as e:
                        continue
        finally:
            self._lock.release()

    def disconnect_all_networks(self, vm, default_network, reserved_networks, logger):
        vnics = self.vnic_service.map_vnics(vm)
        network_for_removal = self.get_networks_on_vnics(
            vm, list(vnics.values()), logger
        )
        update_mapping = [
            VNicDeviceMapper(vnic, vnic, default_network, False, vnic.macAddress)
            for vnic in list(vnics.values())
        ]
        res = self.update_vnic_by_mapping(vm, update_mapping, logger)
        self.erase_network_by_mapping(
            network_for_removal, reserved_networks, logger=logger
        )
        return res

    def _network_is_reserved(self, reserved_networks, network_name):
        return not reserved_networks or network_name not in reserved_networks

    def disconnect_all_networks_if_created_by_quali(
        self, vm, default_network, reserved_networks, logger
    ):
        vnics = self.vnic_service.map_vnics(vm)

        quali_networks = [
            a
            for a in (
                self.vnic_service.get_network_by_device(
                    vm, vnic, self.pyvmomi_service, logger
                )
                for vnic in list(vnics.values())
            )
            if hasattr(a, "name")
            and a.name.lower().startswith("qs_")
            and self._network_is_reserved(reserved_networks, a.name)
        ]

        update_mapping = [
            VNicDeviceMapper(vnic, vnic, default_network, False, vnic.macAddress)
            for vnic in list(vnics.values())
            if self.vnic_service.is_vnic_attached_to_one_of_these_networks(
                vnic, quali_networks
            )
        ]

        res = self.update_vnic_by_mapping(vm, update_mapping, logger)

        logger.info("Updated VM, networks disconnected")

        self.erase_network_by_mapping(quali_networks, reserved_networks, logger=logger)

        return res

    def get_networks_on_vnics(self, vm, vnics, logger):
        return [
            self.vnic_service.get_network_by_device(
                vm, vnic, self.pyvmomi_service, logger
            )
            for vnic in vnics
        ]

    def create_mappings_for_all_networks(self, vm, default_network):
        vnics = self.vnic_service.map_vnics(vm)
        return [
            VNicDeviceMapper(vnic, vnic, default_network, False, vnic.macAddress)
            for vnic in list(vnics.values())
        ]

    def create_mapping_for_network(self, vm, network, default_network):
        condition = (
            lambda vnic: True
            if default_network
            else self.vnic_service.is_vnic_connected(vnic)
        )
        vnics = self.vnic_service.map_vnics(vm)

        mapping = [
            VNicDeviceMapper(vnic, vnic_name, default_network, False, vnic.macAddress)
            for vnic_name, vnic in list(vnics.items())
            if self.vnic_service.is_vnic_attached_to_network(vnic, network)
            and condition(vnic)
        ]
        return mapping

    def disconnect_network(
        self, vm, network, default_network, reserved_networks, logger
    ):
        condition = (
            lambda vnic: True
            if default_network
            else self.vnic_service.is_vnic_connected(vnic)
        )
        vnics = self.vnic_service.map_vnics(vm)
        network_to_remove = self.get_networks_on_vnics(vm, list(vnics.values()), logger)
        mapping = [
            VNicDeviceMapper(vnic, vnic_name, default_network, False, vnic.macAddress)
            for vnic_name, vnic in list(vnics.items())
            if self.vnic_service.is_vnic_attached_to_network(vnic, network)
            and condition(vnic)
        ]

        res = self.update_vnic_by_mapping(vm, mapping, logger)
        self.erase_network_by_mapping(
            network_to_remove, reserved_networks, logger=logger
        )
        return res

    def update_vnic_by_mapping(self, vm, mapping, logger):
        vnics_change = []
        for item in mapping:
            spec = self.vnic_service.vnic_compose_empty(item.vnic)
            self.vnic_service.vnic_attached_to_network(
                spec, item.network, logger=logger
            )
            spec = self.vnic_service.get_device_spec(item.vnic, item.connect)
            vnics_change.append(spec)
        logger.debug("reconfiguring vm: {0} with: {1}".format(vm, vnics_change))
        self.reconfig_vm(device_change=vnics_change, vm=vm, logger=logger)
        return mapping

    def reconfig_vm(self, device_change, vm, logger):
        logger.info("Changing network...")
        task = self.pyvmomi_service.vm_reconfig_task(vm, device_change)
        logger.debug("reconfigure task: {0}".format(task.info))
        res = self.synchronous_task_waiter.wait_for_task(
            task=task, logger=logger, action_name="Reconfigure VM"
        )
        if res:
            logger.debug("reconfigure task result {0}".format(res))
        return res

    @staticmethod
    def destroy_port_group_task(network):
        if network_is_portgroup(network):
            task = DvPortGroupCreator.dv_port_group_destroy_task(network)
            return task
        return None
