import warnings

import pymongo

from tos.utils import accept_string_object_ids
from . import query_helpers as helper


class TaskFinders:

    @accept_string_object_ids
    def find_task_object_by_id(self, object_id):
        """
        Get a single task object.

        This doesn't change the status of the task object.

        :param object_id: the object id
        :type object_id: ObjectId or str
        :returns: task object
        :rtype: dict
        """
        return self.tos.find_one({"_id": object_id})

    def find_one_task_object_by_status(self, statuses):
        """Convenience method."""
        return self.find_one_task_object_by_status_and_stage(statuses=statuses)

    def find_one_task_object_by_stage(self, stages):
        """Convenience method."""
        return self.find_one_task_object_by_status_and_stage(stages=stages)

    def find_one_task_object_by_status_and_stage(self, statuses=None, stages=None, **kwargs):
        """
        Get one of the task objects by status and (optionally) by stage.

        The status of the task object is **always** set to processing when
        using this keyword.

        The filtered results are sorted by date (by default) in ascending
        order so an item with the hightest priority will be returned.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :param sort_condition: custom sort condition of the form
                               `[("_id", pymongo.ASCENDING)]`

        :raises TypeError: when invalid keyword arguments passed
        :returns: task object with the hightest priority.
        :rtype: dict
        """
        if statuses is stages is None:
            raise TypeError("Pass statuses or stages or both.")

        if not kwargs.get("sort_condition"):
            sort_condition = [("_id", pymongo.ASCENDING)]
        elif kwargs.get("sort_condition") == "priority":
            # TODO: is this ever really needed?
            sort_condition = [("priority", pymongo.DESCENDING)]
        else:
            sort_condition = kwargs["sort_condition"]

        amend = kwargs.get("amend", "")
        query = helper.create_query(statuses, stages, amend)

        task_object = self.tos.find_one_and_update(
            query,
            {"$set": {"status": "processing"}},
            sort=sort_condition
        )

        if task_object:
            self.set_task_object_executor(task_object["_id"])
            self.set_task_object_build_number(task_object["_id"])
            self.set_task_object_job_name(task_object["_id"])

        return task_object

    def find_all_failed_task_objects(self):
        """Convenience method."""
        return self.find_all_task_objects_by_status("fail")

    def find_all_task_objects_by_status(self, statuses):
        """Convenience method."""
        return self.find_all_task_objects_by_status_and_stage(statuses=statuses)

    def find_all_task_objects_by_stage(self, stages):
        """Convenience method."""
        return self.find_all_task_objects_by_status_and_stage(stages=stages)

    def find_all_task_objects_by_status_and_stage(self, statuses=None, stages=None):
        """Get all task objects by status and stage.

        The returned list is sorted by priority in descending order so the
        hightest priority item is always the first.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :raises TypeError: when invalid keyword arguments passed
        :returns: list of task objects
        :rtype: list

        Usage:

        >>> find_all_task_objects_by_status_and_stage("pass", 1)
        """
        # FIXME: might be stupid to support both list an str arguments. Maybe always use a list?
        if statuses is stages is None:
            raise TypeError("Pass statuses or stages or both.")

        query = helper.create_query(statuses, stages)
        task_objects = self.tos.find(query).sort([("priority", -1), ])

        return list(task_objects)

    def find_one_task_object_marked_as_manual_and_not_passed(self):
        """
        Get one of the task objects marked as manual.

        The list returned by `find_all_task_objects_marked_as_manual_and_not_passed`
        is sorted by priority so the hightest priority item is
        always the first.

        :returns: manual task object with the hightest priority.
        :rtype: dict
        """
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        task_objects = self.find_all_task_objects_marked_as_manual_and_not_passed()
        if not task_objects:
            return None
        one_object = task_objects[0]

        return one_object

    def find_all_task_objects_marked_as_manual_and_not_passed(self):
        """
        Get all task objects marked to manual handling.

        :returns: list of task objects
        :rtype: list
        """
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        task_objects = self.tos.find(
            {"manual": {"$eq": True},
             "status": {"$ne": "pass"}}
        ).sort([("priority", -1), ])

        return list(task_objects)
