__doc__ = """
Special commands related to windows
"""

import os

from pmake import show_on_help
from pmake import PMakeupModel
from pmake.SessionScript import SessionScript, path


class WindowsSessionScript(SessionScript):

    def __init__(self, model: "PMakeupModel.PMakeModel"):
        super().__init__(model)

    @show_on_help.add_command('windows')
    def test_windows(self, string: str):
        """
        Test if windows commands is loaded
        :param string: the string to echo'ed
        """
        self.echo(string)

    @show_on_help.add_command('windows')
    def add_to_regasm(self, dll: path, architecture: int, regasm_exe: path = None, use_codebase: bool = True, use_tlb: bool = True):
        """
        Add a dll into a regasm (either 32 or 64 bit)
        :param regasm_exe: executable of regasm.
        :param dll: the dll to include in the regasm
        :param architecture: number of bits the processor has. either 32 or 64
        :param use_codebase: if set we will add /codebase
        :param use_tlb: if set, we will add /tlb
        """
        cmds = []

        if regasm_exe is None:
            regasm_exe = self.get_latest_path_with_architecture("regasm", architecture)

        cmds.extend(regasm_exe)
        cmds.extend(dll)
        if use_codebase:
            cmds.extend("/codebase")
        if use_tlb:
            cmds.extend("/tlb")
        self.execute_stdout_on_screen(
            command=[' '.join(cmds)],
            cwd=os.path.dirname(dll)
        )

    @show_on_help.add_command('windows')
    def publish_dotnet_project(self, cwd: path, runtime: str, configuration: str, solution_directory: path) -> None:
        """
        publish a dotnet project.
        For example:

            echo start "PUBLISHING RUNEXTERNALLY" /D "$(SolutionDir)xplan-subsystem-topshelf-service" /WAIT
                dotnet publish
                --runtime "$(PublishRuntime)"
                --configuration "$(PublishConfiguration)"
                /p:SolutionDir="$(SolutionDir)\"

        :param cwd: directory where to call the dotnet publish
        :param runtime: runtime that you will use to publish. Allowed values are 'x86' or 'x64'
        :param configuration: configuration used to build the artifact. Allowed values are 'Debug' or 'Release'
        :param solution_directory: directory containing the a .sln file containing the project that you need to build
        """

        solution_dir = str(solution_directory)
        if not solution_dir.endswith(os.sep):
            solution_dir = solution_dir + os.sep

        self.execute_stdout_on_screen(
            command=[' '.join(["dotnet", "publish", "--runtime", runtime, "--configuration", configuration, f"/p:SolutionDir={solution_dir}"])],
            cwd=cwd,
        )
