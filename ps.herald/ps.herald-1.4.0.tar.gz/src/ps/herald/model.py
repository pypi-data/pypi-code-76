"""The models."""
from sqlalchemy import BigInteger, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# @dataclass
class Log(Base):
    """The logging message.

    The model currently is build around the data structure,
       the standard python logging mechanism uses to send logging
       Events across the **class logging.StreamHandler()**.
    """

    __tablename__ = "log"
    __table_args__ = {
        "sqlite_autoincrement": True
    }  # needed for sqlite. needed for pg ?
    id = Column(Integer, primary_key=True)
    created = Column(String())
    # :e.g. 2015-01-08 10:52:41 currently the time the record
    # is created in the bridge as string sqlite does not support
    # datetime per se here, that is, why the
    # string representation was choosen.
    threadname = Column(String())  # :e.g. MainThread
    api_version = Column(String())  # :e.g. 1.2.44
    package_version = Column(
        String()
    )  # :e.g. The version of the module where logging appeared
    name = Column(String())  # :e.g. Tests
    relativecreated = Column(Float())  # :e.g. 10.5919839592
    process = Column(Integer)  # :e.g. 896
    args = Column(String())  # :e.g. None
    module = Column(String())  # :e.g. t
    funcname = Column(String())  # :e.g. run
    levelno = Column(Integer)  # :e.g. 40
    processname = Column(String())  # :MainProcess
    thread = Column(BigInteger)  # :e.g. 140735286908888
    msecs = Column(Float())  # :e.g. 616.5919839592
    message = Column(String())  # :e.g. "The msg of a log.info statement"
    exc_text = Column(String())  # :e.g. None
    exc_info = Column(String())  # :e.g. None
    stack_info = Column(String())  # :e.g. None
    pathname = Column(String())  # :e.g. /Users/setzt/Haufe/basic_package
    filename = Column(String())  # :e.g. Basic.py
    asctime = Column(String())  # :e.g. ????
    levelname = Column(String())  # :INFO
    lineno = Column(Integer)  # :e.g. 42
    # These are "extra fields" not in the standard python logging
    produkt_id = Column(String(10))  # :e.g. PRODUKT_ID
    system_id = Column(String(10))  # :e.g. SYSTEM_ID
    sub_system_id = Column(String(10))  # :e.g. SUB_SYSTEM_ID
    sub_sub_system_id = Column(String(10))  # :e.g. SUB_SUB_SYSTEM_ID
    user_spec_1 = Column(String(10))  # :e.g. User_specific_value_one
    user_spec_2 = Column(String(10))  # :e.g. User_specific_value_two
    summary = Column(String(70))  # :e.g. concatenation of the before values

    def as_dict(self):
        """Return row as dict."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """Return row as beein used in a´html table."""
        d = {}
        d["created"] = self.created
        d["package_version"] = self.package_version
        d["module"] = self.module
        d["lineno"] = self.lineno
        d["funcname"] = self.funcname
        try:
            d["lower_levelname"] = self.levelname.lower()
        except Exception:
            d["lower_levelname"] = str(self.levelno)

        d["levelname"] = self.levelname
        d["message"] = self.message
        d["exc_text"] = self.exc_text
        d["stack_info"] = self.stack_info
        d["system_id"] = self.system_id
        d["sub_system_id"] = self.sub_system_id
        d["sub_sub_system_id"] = self.sub_sub_system_id
        d["user_spec_1"] = self.user_spec_1
        d["user_spec_2"] = self.user_spec_2
        d["produkt_id"] = self.produkt_id

        return (
            '<tr class="%(lower_levelname)s"> \
                <td>%(created)s</td> \
                <td>%(levelname)s</td> \
                <td>%(system_id)s<br>%(sub_system_id)s\
                    <br>%(sub_sub_system_id)s</td> \
                <td>%(produkt_id)s<br>%(user_spec_1)s\
                    <br>%(user_spec_2)s</td>\
                <td>%(module)s %(package_version)s<br>\
                    %(funcname)s<br>line: %(lineno)s<br></td> \
                <td>%(message)s</td> \
                <td>%(exc_text)s</td> \
                <td>%(stack_info)s</td> \
                </tr>'
            % d
        )


class HeartBeat(Base):
    """Store the HeartBeat of the different systems."""

    __tablename__ = "heartbeat"
    __table_args__ = {
        "sqlite_autoincrement": True
    }  # needed for sqlite. needed for pg ?

    id = Column(Integer, primary_key=True)
    newest_heartbeat = Column(String())  # :e.g. 2015-01-08 10:52:41
    system_id = Column(String(10), unique=True)  # :e.g. SYSTEM_ID

    def __repr__(self):
        """Return heartbeat repr."""
        return "<system_id: %r <heartbeat: %r" % (
            self.system_id,
            self.newest_heartbeat,
        )
