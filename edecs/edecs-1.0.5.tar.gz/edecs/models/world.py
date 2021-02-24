from copy import deepcopy
from asyncio import iscoroutinefunction
from .exceptions import *
from .message import message as msg
from .event import event


class world():
    ''' World class'''

    entities = [] # [id: entity]
    components = {} # {type: ent_id: comp_id: comp}
    systems = {} # {type: system}

    systems_to_start = []
    systems_to_finish = []

    dead_entities = []
    components_del_queue = []

    loop = None

    @classmethod
    def create_system(world, system):
        if world.systems.get(system.type) is not None:
            raise SystemTypeAlreadyExists(system)

        if system.initialized:
            raise SystemAlreadyInitialized(system)

        world.systems[system.type] = system
        system.initialized = True

        msg.subscribe(system.type, system.on_message)
        world.systems_to_start.append(system)


    @classmethod
    def delete_system(world, system):
        if isinstance(system, str):
            sys_name = system
            system = world.systems.get(system)

            if system is None:
                raise SystemDoesNotExist(sys_name)

        if world.systems.get(system.type) is None:
            raise SystemDoesNotExist(system)

        if not system.initialized:
            raise SystemIsNotInitialized(system)

        msg.unsubscribe(system.type)
        event.unsubscribe_system(system)
        world.systems_to_finish.append(system)

        world.systems.pop(system.type)
        system.initialized = False

    @classmethod
    def create_entity(world, entity):
        if entity.initialized:
            raise EntityAlreadyExists(entity)

        ent_id = -1

        if len(world.dead_entities) > 0:
            ent_id = world.dead_entities.pop(0)
            world.entities[ent_id] = entity

        else:
            ent_id = len(world.entities)
            world.entities.append(entity)

        entity.id = ent_id
        entity.initialized = True

        for comp_id, component in entity.default_components.items():
            component = deepcopy(component)
            world.add_component(entity, comp_id, component)

    @classmethod
    def get_entity(world, entity_id):
        if entity_id is None or entity_id >= len(world.entities) or entity_id < 0:
            return None

        return world.entities[entity_id]

    @classmethod
    def get_entities(world):
        for entity in world.entities:
            if entity is not None:
                yield entity

    @classmethod
    def delete_entity(world, entity):
        if isinstance(entity, int):
            entity_id = entity
            entity = world.get_entity(entity)

            if entity is None:
                raise EntityDoesNotExist(entity_id)

        elif world.get_entity(entity.id) is None:
            raise EntityDoesNotExist(entity)

        for component in entity.components.values():
            world.delete_component(component)

        world.entities[entity.id] = None
        world.dead_entities.append(entity.id)
        entity.initialized = False

    @classmethod
    def add_component(world, entity, component_id, component):
        if isinstance(entity, int):
            entity_id = entity
            entity = world.get_entity(entity)

            if entity is None:
                raise EntityDoesNotExist(entity_id)

        elif world.get_entity(entity.id) is None:
            raise EntityDoesNotExist(entity)

        if component.initialized:
            raise ComponentAlreadyHaveEntity(component)

        if world.components.get(component.type) is None:
            world.components[component.type] = {}

        type_components = world.components[component.type]

        if type_components.get(entity.id) is None:
            type_components[entity.id] = {}

        if entity.components.get(component_id) is not None:
            old_component = entity.components[component_id]
            old_component.id = None
            old_component.entity = None

        entity_type_components = type_components[entity.id]
        entity_type_components[component_id] = component

        component.id = component_id
        component.entity = entity
        entity.components[component_id] = component


    @classmethod
    def get_component(world, entity, component_id):
        if isinstance(entity, int):
            entity_id = entity
            entity = world.get_entity(entity)

            if entity is None:
                raise EntityDoesNotExist(entity_id)

        return entity.components.get(component_id)

    @classmethod
    def get_components(world, component_type=None):
        if component_type is None:
            for type_components in world.components.values():
                for entity_components in type_components.values():
                    for component in entity_components.values():
                        if component not in world.components_del_queue:
                            yield component

        else:
            type_components = world.components.get(component_type)

            if type_components is None:
                return {}

            for entity_components in type_components.values():
                for component in entity_components.values():
                    if component not in world.components_del_queue:
                        yield component

    @classmethod
    def delete_component(world, component, immediately=False):
        if not immediately:
            if component not in world.components_del_queue:
                world.components_del_queue.append(component)
            return

        if not component.initialized:
            raise ComponentHasNoEntity(component)

        entity = component.entity

        del entity.components[component.id]
        del world.components[component.type][entity.id][component.id]

        if len(world.components[component.type][entity.id]) == 0:
            del world.components[component.type][entity.id]

        if len(world.components[component.type]) == 0:
            del world.components[component.type]

        component.id = None
        component.entity = None

    @classmethod
    def update(world):
        while len(world.components_del_queue) > 0:
            del_component = world.components_del_queue.pop(0)
            world.delete_component(del_component, immediately=True)

        while len(world.systems_to_start) > 0:
            system = world.systems_to_start.pop(0)
            system.on_start()

        while len(world.systems_to_finish) > 0:
            system = world.systems_to_finish.pop(0)
            system.on_finish()

        for system in world.systems.values():
            system.on_update()

    @classmethod
    def async_update(world, loop):
        if loop != world.loop:
            world.loop = loop

        while len(world.components_del_queue) > 0:
            del_component = world.components_del_queue.pop(0)
            world.delete_component(del_component, immediately=True)

        while len(world.systems_to_start) > 0:
            system = world.systems_to_start.pop(0)
            if iscoroutinefunction(system.on_start):
                loop.create_task(system.on_start())

            else:
                func = world.create_async_func(system.on_start)
                loop.create_task(func())

        while len(world.systems_to_finish) > 0:
            system = world.systems_to_finish.pop(0)
            if iscoroutinefunction(system.on_finish):
                loop.create_task(system.on_finish())

            else:
                func = world.create_async_func(system.on_finish)
                loop.create_task(func())

        for system in world.systems.values():
            if not system.is_updating:
                system.is_updating = True
                func = world.create_async_update_func(system, system.on_update)
                loop.create_task(func())

    @staticmethod
    def create_async_update_func(system, func):
        if iscoroutinefunction(func):
            async def async_func():
                await func()
                system.is_updating = False

            return async_func

        else:
            async def async_func():
                func()
                system.is_updating = False

            return async_func

    @staticmethod
    def create_async_func(func):
        async def async_func():
            func()
        return async_func
