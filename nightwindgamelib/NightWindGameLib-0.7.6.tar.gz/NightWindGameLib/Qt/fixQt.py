class FixPySide2:
    def analyse_code(self, contents: str) -> tuple:
        lines = contents.splitlines(keepends=True)
        # locate pyside_package_dir line index
        pkg_dir = 'os.path.abspath(os.path.dirname(__file__))'
        for index, line in enumerate(lines):
            if pkg_dir in line:
                break

        # return lines, line index, indentation
        return lines, index, ' ' * (len(line.rstrip()) - len(line.strip()))

    def insert_lines(self, contents: str) -> list:
        lines, position, indentation = self.analyse_code(contents)
        new_lines = (
                lines[position] + '\n' +
                indentation + '# add platforms plugin to PATH\n' +
                indentation + 'platforms_dir = ' +
                'os.path.join(pyside_package_dir, "plugins", "platforms")\n' +
                indentation +
                'os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir\n')

        # insert lines
        lines[position] = new_lines
        return lines

    def add_plugins_to_PATH(self, file_path):
        # open __init__.py
        with open(file_path, encoding='utf-8') as f:
            contents = f.read()

        # insert lines
        lines = self.insert_lines(contents)

        # save changes to __init__.py
        code = ''.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

    def start_fix(self):
        """Glitch fixing entry."""
        import PySide2
        PySide2_init_module = PySide2.__file__
        self.add_plugins_to_PATH(PySide2_init_module)


class FixPySide6:
    def analyse_code(self, contents: str) -> tuple:
        lines = contents.splitlines(keepends=True)
        # locate pyside_package_dir line index
        pkg_dir = 'os.path.abspath(os.path.dirname(__file__))'
        for index, line in enumerate(lines):
            if pkg_dir in line:
                break

        # return lines, line index, indentation
        return lines, index, ' ' * (len(line.rstrip()) - len(line.strip()))

    def insert_lines(self, contents: str) -> list:
        lines, position, indentation = self.analyse_code(contents)
        new_lines = (
                lines[position] + '\n' +
                indentation + '# add platforms plugin to PATH\n' +
                indentation + 'platforms_dir = ' +
                'os.path.join(pyside_package_dir, "plugins", "platforms")\n' +
                indentation +
                'os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir\n')

        # insert lines
        lines[position] = new_lines
        return lines

    def add_plugins_to_PATH(self, file_path):
        # open __init__.py
        with open(file_path, encoding='utf-8') as f:
            contents = f.read()

        # insert lines
        lines = self.insert_lines(contents)

        # save changes to __init__.py
        code = ''.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

    def start_fix(self):
        """Glitch fixing entry."""
        import PySide6
        PySide6_init_module = PySide6.__file__
        self.add_plugins_to_PATH(PySide6_init_module)
