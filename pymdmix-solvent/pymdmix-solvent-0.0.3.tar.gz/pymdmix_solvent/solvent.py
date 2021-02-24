import os
import warnings
from argparse import ArgumentParser, Namespace
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from parmed.amber import AmberOFFLibrary
from pymdmix_core.orm import BaseModel
from pymdmix_core.plugin.crud import ActionDelete, CRUDPlugin, parse_file_from_args


class ActionDeleteSolvent(ActionDelete):

    def run(self, args: Namespace) -> None:
        session = self.parent_plugin.session
        model_class = self.parent_plugin.CLASS
        query = session.query(model_class).filter(model_class.id.in_(args.id))
        for model in query.all():
            session.delete(model)
        session.commit()


PROBES_TO_TYPES_ASSOCIATION_TABLE = Table(
    'probes_to_types_association',
    BaseModel.metadata,
    Column('probe_id', String, ForeignKey("solvent_probes.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column('probe_type_id', String, ForeignKey("solvent_probe_types.id"))
)


class Solvent(BaseModel):
    __tablename__ = "solvents"
    id = Column(String, primary_key=True)
    info = Column(String)
    unit = Column(String)
    off_file = Column(LargeBinary)
    residue = Column(String)
    probes = relationship("Probe", cascade="all, delete, delete-orphan")

    def __str__(self):
        return self.id

    def __repr__(self) -> str:
        msg = [f"[{self.id}]: {self.info}"]
        msg += [f"\t{probe.__repr__()}" for probe in self.probes]
        return "\n".join(msg)


class Probe(BaseModel):
    __tablename__ = "solvent_probes"

    id = Column(String, primary_key=True)
    solvent = Column(
        String,
        ForeignKey(
            "solvents.id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        primary_key=True,
        nullable=False
    )
    mask = Column(String)
    types = relationship("ProbeType", secondary=PROBES_TO_TYPES_ASSOCIATION_TABLE)

    def __repr__(self) -> str:
        return f"[{self.id}]: {','.join([t.id for t in self.types])}"


class ProbeType(BaseModel):
    __tablename__ = "solvent_probe_types"
    id = Column(String, primary_key=True)


class SolventPlugin(CRUDPlugin):

    NAME = "solvent"
    HELP_STRING: str = ""
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_solvent.yml"
    ALLOW_EMPTY_ACTION = False
    CLASS = Solvent

    def __init__(self, master_parser: ArgumentParser) -> None:
        super().__init__(master_parser)

    def init_actions(self, action_subparser):
        super().init_actions(action_subparser)
        self.register_action(ActionDeleteSolvent(action_subparser, self))

    def init_parser(self) -> None:
        return super().init_parser()

    def run(self, args: Namespace) -> None:
        return super().run(args)

    def factory(self, args: Namespace) -> Solvent:
        fields = parse_file_from_args(args)
        if fields is None:
            raise ValueError("unable to read config file for solvent")
        config_file = args.json if args.json is not None else args.yaml
        models = []
        for solvent_id, data in fields.items():
            off_file_data = self._get_off_data(config_file, data)
            solvent_data = {
                "id": solvent_id,
                "info": data.get("info"),
                "off_file": off_file_data,
                "unit": data.get("unit"),
                "residue": data.get("residue")
            }
            solvent = Solvent(**solvent_data)
            self.session.add(solvent)
            self._probes_factory(data, solvent)
            models.append(solvent)
        return models if len(models) > 0 else None

    def _probes_factory(self, data, solvent):
        for probe_id, probe_fields in data.get("probes", {}).items():
            probe_data = {
                "id": probe_id,
                "solvent": solvent.id,
                "mask": probe_fields.get("mask"),
            }
            probe = Probe(**probe_data)
            self.session.add(probe)
            for probe_type in probe_fields.get("types", []):
                current = self.session.query(ProbeType).filter(ProbeType.id == probe_type).first()
                if current is None:
                    current = ProbeType(id=probe_type)
                    self.session.add(current)
                probe.types.append(current)
            solvent.probes.append(probe)
        self.session.commit()
        return solvent

    def _get_off_data(self, config_file, values):
        off_file = values["off_file"]
        if not os.path.exists(off_file):
            base_path = os.path.dirname(config_file)
            off_file = os.path.join(base_path, off_file)
        # this is a format check, to ensure the file passed is a properly formed OFF file
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            AmberOFFLibrary().parse(off_file)
        off_file_data = None
        with open(off_file, 'rb') as file:
            off_file_data = file.read()
        return off_file_data
