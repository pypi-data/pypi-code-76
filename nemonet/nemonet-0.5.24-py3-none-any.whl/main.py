# Created by Jan Rummens at 8/01/2021
from nemonet.runner.vision_runner import Runner
from nemonet.plugin.handle_zephyr import merge_json_xml
from nemonet.engines.reporter import Reporter
from nemonet.cfg.config import Configuration
import typer
import sys
import traceback

app = typer.Typer()

@app.command()
def scenario(name: str, useconfig: bool = False):
    try:
        if useconfig:
            runner = Runner(runner_config="runner_config.json")
        else:
            runner = Runner()
        runner.execute_scenario(name)
    except ValueError:
        typer.echo(f"invalid commandline")
    except FileNotFoundError as e:
        typer.echo(e)
    except Exception as err:
        traceback.print_tb(err.__traceback__)
    finally:
        reporter = Reporter()
        if runner.scenario_passed():
            #reporter.publish(name, Reporter.status_passed)
            pass
        else:
            #reporter.publish(name, Reporter.status_failed)
            runner.driver.close()
        runner.turn_off_recording()



@app.command()
def zephyr(scenario:str):
    merge_json_xml(scenario, jira_flag=True)
