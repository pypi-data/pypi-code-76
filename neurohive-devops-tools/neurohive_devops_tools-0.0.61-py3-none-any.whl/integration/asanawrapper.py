import asana
from enum import Enum


class TaskStatuses(Enum):
    IN_PROGRESS = '1177715646699485'
    DESIGN_REVIEW = '1193700203212323'
    BUILD_REVIEW = '1177715646699486'


class AsanaWrapper:
    def __init__(self, token, workspace):
        self.client = asana.Client.access_token(token)
        self.workspace = workspace

    def _get_custom_field_enum(self, project_id, field_name):
        result = self.client.custom_field_settings.get_custom_field_settings_for_project(project_id)
        filtered = filter(lambda item: field_name in item.get('custom_field').get('name'), result)
        if filtered:
            enums_data = next(filtered)
            enum_opts = map(lambda item: (item['gid'], item['name']), enums_data['custom_field']['enum_options'])
            print(f'Name: {field_name} {enums_data["custom_field"]["gid"]}')
            print(list(enum_opts))

    def switch_status(self, task_name, status_field_id, status: TaskStatuses):
        task_id = self._find_task(task_name)
        if task_id:
            result = self.client.tasks.update_task(  # noqa: F841
                task_id,
                {
                    'custom_fields': {
                        status_field_id: status.value
                    }
                }
            )

    def comment_task(self, task_name, comment):
        t_gid = self._find_task(task_name)
        self._create_story(t_gid, comment)

    def _find_task(self, task_name):
        result = self.client.typeahead.typeahead_for_workspace(
            self.workspace,
            {
                'resource_type': 'task',
                'query': task_name,
                'count': 1
            }
        )
        tasks = list(result)
        if tasks:
            return tasks[0]['gid']

    def _create_story(self, task_gid, html_text):
        result = self.client.stories.create_story_for_task(  # noqa: F841
            task_gid,
            {
                'html_text': html_text
            }
        )
