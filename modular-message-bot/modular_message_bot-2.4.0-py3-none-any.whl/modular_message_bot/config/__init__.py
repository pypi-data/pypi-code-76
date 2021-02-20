"""
# Global Config (ENVs)

| Key | Required | Description |
|---|---|---|
| SCHEDULER_TIMEZONE | No | The timezone to use. The default is 'utc'. See http://pytz.sourceforge.net/.
Note: This is also used for datetime zone default |
| RUN_DETAILS_B64 | No | A base64 encoded job YAML definition. E.g. `base64 config/jobs.yml` |
| RUN_DETAILS_FILE | No | Location of the job YAML file |
| RUN_DETAILS_DIR | No | A directory we will look for all yml or yaml files and load jobs from |

## Config and Interpolation in Jobs
The config comes from envs as well as secret files. It should be easy to extend though.
You can use config to replace parts of your jobs file as well (note: it is case-sensitive!)

| Name | Type | Notes |
|---|---|---|
| Runtime substitution | `${CONFIG_NAME}` | Only runs once on application start but is very flexible |
| Dynamic substitution | `$[CONFIG_NAME]` | Only works in module parameters but is loaded everytime |

"""
