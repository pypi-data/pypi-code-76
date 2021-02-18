
class ModSavedAttributes:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.input_attributes = {}
        # Load configuration file
        with open(self.input_path, "r") as input:
            self.input_attributes = yaml.load(input, Loader=yaml.Loader)

    def insert_column(self, attribute_group, device, attribute, insert_at=None, preset_group=None):
        for pg in self.get_preset_groups():
            if preset_group is not None and preset_group != pg:
                continue
            ag = self.input_attributes['Preset groups'][pg][attribute_group]
            new_column = (device, attribute)
            if new_column not in ag["columns"]:
                if insert_at is None:
                    ag["columns"].append(new_column)
                else:
                    ag["columns"].insert(insert_at, new_column)
            insert_at_row = ag["columns"].index(new_column) + 2
            for row in ag["rows"]:
                row.insert(insert_at_row, None)

    def reverse_rows(self):
        for pg in self.get_preset_groups():
            for ag in self.input_attributes['Preset groups'][pg].values():
                ag["rows"] = list(reversed(ag["rows"]))

    def get_preset_groups(self):
        return list(self.input_attributes['Preset groups'].keys())

    def get_attribute_groups(self, preset_group):
        return list(self.input_attributes['Preset groups'][preset_group].keys())

    def save(self):
        with open(self.output_path, "w") as fp:
            yaml.dump(self.input_attributes, fp)

if __name__ == "__main__":
    import argparse
    import os
    import signal

    import oyaml as yaml

    import kamzik3
    from kamzik3.snippets.snippetsWidgets import init_qt_app

    # Parse arguments from commandline
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input path for saved attributes",
                        default="./saved_attributes.att")
    parser.add_argument("--output", help="Path where to save new modified file",
                        default="./saved_attributes_mod.att")
    parser.add_argument("--chdir", help="Path to active directory",
                        default="./")
    args = parser.parse_args()

    # Set active directory
    os.chdir(args.chdir)

    mod = ModSavedAttributes(args.input, args.output)
    mod.reverse_rows()
    # mod.insert_column("Beamstop", "XA", ["Position", "Value"])
    # mod.insert_column("Beamstop", "YA", ["Position", "Value"])
    # mod.insert_column("Sample", "Roll-SAM", ["Position", "Value"])
    mod.save()
