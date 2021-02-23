# <copyright file="snowconvert_helpers.py" company="Mobilize.Net">
#     Copyright (C) Mobilize.Net info@mobilize.net - All Rights Reserved
#
#     This file is part of the Mobilize Frameworks, which is
#     proprietary and confidential.
#
#     NOTICE:  All information contained herein is, and remains
#     the property of Mobilize.Net Corporation.
#     The intellectual and technical concepts contained herein are
#     proprietary to Mobilize.Net Corporation and may be covered
#     by U.S. Patents, and are protected by trade secret or copyright law.
#     Dissemination of this information or reproduction of this material
#     is strictly forbidden unless prior written permission is obtained
#     from Mobilize.Net Corporation.
# </copyright>

import sys
import logging
import subprocess
import datetime
import snowflake.connector
from os import getenv
from os import access
from os import R_OK
from os import system
from os import makedirs, path, stat
from functools import singledispatch
import re
import csv
import atexit
import traceback
import inspect



snow_debug_colors = getenv("SNOW_DEBUG_COLOR","").strip().upper()

if snow_debug_colors:
    import termcolor

def colored(text, color="blue"):
    if (snow_debug_colors == "YES" or snow_debug_colors == "ON" or snow_debug_colors == "TRUE"):
        return termcolor.colored(text,color)
    return text

# global status values
max_errors = 1
current_error_count = 0
activity_count = 0
error_code = 0
error_level = 0
warning_code = 0
system_return_code = 0
quit_application_already_called = False

# severities dictionary
_severities_dictionary = dict()
_default_error_level = 8

# last executed sql statement
_previous_executed_sql = ""

has_passed_variables = False
passed_variables = {}

def configure_log():
    logging.basicConfig(
        filename='snowflake_python_connector.log',
        level=logging.DEBUG,
        filemode='w')

def get_from_args_or_environment(arg_pos, env_variable_name, args):
    if (arg_pos < len(args)):
        return args[arg_pos]
    env_value = getenv(env_variable_name)
    return env_value

def get_argkey(astr):
     if astr.startswith('--param-'):
         astr = astr[8:astr.index('=')]
     return astr

def get_argvalue(astr):
     if astr.startswith('--param-'):
         astr = astr[astr.index('=')+1:]
     return astr

def read_param_args(args):
    script_args = [item for item  in args if item.startswith("--param-")]
    dictionary = {}
    if len(script_args) > 0:
        dictionary = { get_argkey(x) : get_argvalue(x) for x in args}
        if len(dictionary) != 0:
            has_passed_variables = True
            print("Using variables")
            print(dictionary)
    return dictionary
    


def expandvars(path, params, skip_escaped=False):
    """Expand environment variables of form $var and ${var}.
       If parameter 'skip_escaped' is True, all escaped variable references
       (i.e. preceded by backslashes) are skipped.
       Unknown variables are set to 'default'. If 'default' is None,
       they are left unchanged.
    """
    def replace_var(m):
        varname = m.group(3) or m.group(2)
        passvalue = params.get(varname, None)
        return getenv(varname, m.group(0) if passvalue is None else passvalue)
    reVar = (r'(?<!\)' if skip_escaped else '') + r'(\$|\&)(\w+|\{([^}]*)\})'
    return re.sub(reVar, replace_var, path)

def expands_using_params(statement, params):
    def replace_var(m):
        varname = m.group(1)
        passvalue = params.get(varname, None)
        if (passvalue is None):
            return m.group(0)
        else:
            return str(passvalue)
    reVar = r'\{([^}]*)\}'
    return re.sub(reVar, replace_var, statement) 


def expandvar(str):
    return expandvars(str,passed_variables)

opened_connections = []

def log_on(user=None, password=None, account=None, database=None,warehouse=None,role=None, login_timeout = 10):
    global error_code
    # exclude arguments passed inline to the script
    args = [item for item  in sys.argv if not item.startswith("--param-")]
    if (user is None):
        user = get_from_args_or_environment(1, "SNOW_USER", args)
    if (password is None):
        password = get_from_args_or_environment(2, "SNOW_PASSWORD", args)
    if (account is None):
        account = get_from_args_or_environment(3, "SNOW_ACCOUNT", args)
    if (database is None):
        database = get_from_args_or_environment(4, "SNOW_DATABASE", args)
    if (warehouse is None):
        warehouse = get_from_args_or_environment(5, "SNOW_WAREHOUSE", args)
    if (role is None):
        role = get_from_args_or_environment(6, "SNOW_ROLE", args)
    query_tag = getenv("SNOW_QUERYTAG",None)
    if query_tag is None:
        frm = inspect.stack()[1]
        query_tag = path.basename(frm.filename)
    c = None
    try:
        c = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            database=database,
            warehouse = warehouse,
            role=role,
            login_timeout=login_timeout,
            session_parameters={
                'QUERY_TAG': query_tag
            }
        )
    except Exception as e:
        print(colored('*** Failure: logon failed :','red') + str(e))
        error_code = 333
        quit_application(error_code)
    if c:
        opened_connections.append(c)
        error_code = 0
    return c

def at_exit_helpers():
    print("Script done >>>>>>>>>>>>>>>>>>>>")
    for c in opened_connections:
        if not c.is_closed():
            c.close()
    quit_application()

def exception_hook(exctype, value, traceback):
    traceback_formatted = traceback.format_exception(exctype, value, traceback)
    traceback_string = colored("*** Failure: " + "".join(traceback_formatted),'red')
    print(traceback_string, file=sys.stderr)
    quit_application(1)

def using(*argv):
    using_dict = {}
    Import.using(using_dict,*argv)
    return using_dict

def import_file(filename, separator = ' '):
    return Import.file(filename, separator)

def import_reset():
    return Import.reset()

def execute_sql_statement(sql_string, con, using=None):
    global activity_count
    global current_error_count
    global max_errors
    global error_code

    cur = con.cursor()
    try:
        error_code = 0
        print(colored("Executing: ",'blue') + colored(sql_string,'cyan'))
        if ("$" in sql_string or "&" in sql_string):
            print ("Expanding variables in SQL statement")
            sql_string = expandvars(sql_string, passed_variables)
            print (colored("Expanded string: ") + colored(sql_string,'green'))
        if (using is not None):
                #we need to change variables from {var} to %(format)
                sql_string = re.sub(r'\{([^}]*)\}',r'%(\1)',sql_string)
                print(f"using parameters {using}")
                #sql_string = expands_using_params(sql_string, using)
                #print(f"Applying using vars {sql_string}")
        cur.execute(sql_string, params=using)
        activity_count = cur.rowcount
        if activity_count and activity_count >= 1:
            _print_result_set(cur)
        else:
            if (Export.expandedfilename is not None):
                _print_result_set(cur)
    except snowflake.connector.errors.ProgrammingError as e:
        current_error_count = current_error_count + 1
        if "syntax error" in e.msg:
            regex = r"syntax error line (\d+) at position (\d+)"
            matches = re.finditer(regex, e.msg, re.MULTILINE)
            #first_error = True
            error_fragment = "SYNTAX ERROR:\n"
            sql_lines = sql_string.splitlines()
            last_line = -1       
            for matchNum, match in enumerate(matches, start=1):
                    line = int(match.groups()[0])-1
                    column = int(match.groups()[1])
                    if line != last_line:
                        error_line = sql_lines[line]
                        error_line = error_line[:column] + colored(error_line[column:],'red')
                        error_fragment = error_fragment + "{0:0>2d},{1:0>2d}:{2}\n".format(line, column, error_line)
                    last_line = line
            print(error_fragment)
        _handle_sql_error(e)
    except: # catch *all* exceptions
        current_error_count = current_error_count + 1
        e = sys.exc_info()
        msg = colored("*** Failure running statement",'red')
        print(msg)
        print(e)
    finally:
        _previous_executed_sql = sql_string
        cur.close()
        if current_error_count >= max_errors:
            print(colored('*** Failure: reached max error count {0}'.format(max_errors),'red'))
            quit_application(1)


def repeat_previous_sql_statement(con, n = 1):
    if _previous_executed_sql == "":
        if n == 0:	
            n = 1
        for rep in xrange(n):
            execute_sql_statement(_previous_executed_sql, con)
    else:
        print("Warning: No previous SQL request.")


def _print_result_set(cur):
    if (Export.expandedfilename is None):
        # if there is not export file set then print to console
        print("Printing Result Set:")
        print(','.join([col[0] for col in cur.description]))
        for row in cur:
            print(','.join([str(val) for val in row]))
        print()
    else:
        print(">>>>>> Exporting to " + Export.expandedfilename)
        reportdir = path.dirname(Export.expandedfilename)
        makedirs(reportdir, exist_ok=True)
        with open(Export.expandedfilename, 'a') as f:
            for row in cur:
                allarenone = all(v is None for v in row)
                if (allarenone):
                    print("Row is 'None' it will not be exported")
                else:
                    rowval=Export.separator.join([str(val) for val in row])
                    print(rowval, file=f)


def _handle_sql_error(e):
    global error_code, error_level
    error_code = e.errno
    if error_code not in _severities_dictionary or _severities_dictionary[error_code] != 0:
        msg = colored("*** Failure " + str(e),'red')
        print(msg, file=sys.stderr)
        if error_code in _severities_dictionary:
            error_level = max(error_level, _severities_dictionary[error_code])
        else:
            error_level = max(error_level, _default_error_level)


@singledispatch
def set_error_level(arg, severity_value):
    "Invoked set_error_level with arg={0}, severity_value={1}".format(arg, severity_value)


@set_error_level.register(int)
def _(arg, severity_value):
    _severities_dictionary[arg] = severity_value


@set_error_level.register(list)
def _(arg, severity_value):
    for code in arg:
        _severities_dictionary[code] = severity_value


def set_default_error_level(severity_value):
    global _default_error_level
    _default_error_level = severity_value


def os(args):
    global system_return_code
    system_return_code = system(args)

## reads the given filename and executes the code
def readrun(line, skip=0):
    expandedpath = path.expandvars(line)
    if path.isfile(expandedpath):
        return open(expandedpath).readlines()[skip:]
    else:
        return []


def remark(arg):
    print(arg)

def get_error_position():
    stack = inspect.stack()
    important_frames = []
    for i in range(len(stack)):
        current_stack = stack[i]
        if current_stack.filename.endswith(__name__ + ".py"):
            # we skip the first one because is the frame for this function
            # now we take this element and the next max 5 ones
            next_frames = i + 5 if i + 5 < len(stack) else len(stack)
            important_frames.extend(stack[i+1:next_frames])
    stack_trace = "Error at:\n"
    for frame in important_frames:
        stack_trace = stack_trace + "{0.filename}:{0.lineno} function: {0.function} \n".format(frame)
    return stack_trace

def quit_application(code=None):
    global quit_application_already_called
    if quit_application_already_called:
        return
    quit_application_already_called = True
    code = code or error_level
    print(colored(f"Error Code {code}",'red'))
    if code != 0:
        stack_trace = get_error_position();
        print(colored(stack_trace,'red'))
    sys.exit(code)


def import_data_to_temptable(tempTableName, inputDataPlaceholder, con):
    sql = """COPY INTO {} FROM {}  FILE_FORMAT = ( TYPE=CSV SKIP_HEADER = 1 ) ON_ERROR = CONTINUE""".format(tempTableName, inputDataPlaceholder)
    execute_sql_statement(sql, con)

def drop_transient_table(tempTableName, con):
    sql = """DROP TABLE {}""".format(tempTableName)
    execute_sql_statement(sql, con)

def file_exists_and_readable(filename):
    return access(path.expandvars(filename),R_OK)

def exec_os(command):
    print("executing os command: {0}".format(command))
    return subprocess.getoutput(command)

def simple_fast_load(con,target_schema,filepath,stagename,target_table_name):
   ## expand any environment var
   target_schema = expandvar(target_schema)
   filepath = expandvar(filepath)
   filename = path.basename(filepath)
   stagename = expandvar(stagename)
   target_table_name = expandvar(target_table_name)
   execute_sql_statement(f""" USE SCHEMA {target_schema} """, con)
   print(f"Putting file {filepath} into {stagename}...")
   con.cursor().execute(f"PUT file://{filepath} @{stagename} OVERWRITE = TRUE")
   print(f"Done put file...ErrorCode {error_code}")
   print(">>>Copying into...")
   execute_sql_statement(f"""
   COPY INTO {target_schema}.{target_table_name}
   FROM @{stagename}/{filename}
   FILE_FORMAT = ( TYPE=CSV SKIP_HEADER = 1 )
   ON_ERROR = CONTINUE""", con)
   print(f"<<<Done copying. ErrorCode {error_code}")
   print(f">>>Creating temp table CTE_{target_table_name}")
   sql = f"CREATE TABLE {target_schema}.CTE_{target_table_name}  AS SELECT DISTINCT * FROM {target_schema}.{target_table_name}"
   execute_sql_statement(sql, con)
   print(f"<<<Done creating temp table. ErrorCode {error_code}")
   print(f">>>Droping old {target_table_name}")
   sql = f"DROP TABLE {target_schema}.{target_table_name}"
   execute_sql_statement(sql, con)
   print(f"<<<Done droping old table. ErrorCode {error_code}")
   print(f">>>Renaming old CTE_{target_table_name}")
   sql = f"ALTER TABLE {target_schema}.CTE_{target_table_name} RENAME TO {target_schema}.{target_table_name}"
   execute_sql_statement(sql, con)
   print(f"<<<Done droping old table. ErrorCode {error_code}")

atexit.register(at_exit_helpers)

def exception_hook(exctype, value, tback):
    print(colored(f"*** Failure: {value}",'red'), file=sys.stderr)
    traceback_formatted = traceback.format_exception(exctype, value, tback)
    traceback_string = "".join(traceback_formatted)
    print(traceback_string, file=sys.stderr)
    quit_application(1)

sys.excepthook = exception_hook
   
class Import:
    expandedfilename=None
    separator=' '
    reader = None
    no_more_rows=False
    read_obj = None

    def file(file, separator=' '):

        Import.separator = separator
        Import.expandedfilename = path.expandvars(file)
        Import.reader=None
        if (not Import.read_obj is None):
            Import.read_obj.close()
        Import.read_obj=None
        Import.no_more_rows = False

    def using(globals,*argv):
        print (argv)
        try:
            variables_li = [] 
            types_li = []
            i = 0
            while i < len(argv):
                elem = argv[i]
                if (i % 2 == 0): 
                    variables_li.append(elem) 
                else: 
                    types_li.append(elem)
                i += 1
            i = 0
            # init the global variables for the using clause
            while i < len(variables_li):
                initvalue = None
                if (types_li[i].startswith("DECIMAL")):
                    initvalue = 0
                else:
                    if (types_li[i].startswith("DATE")):
                        initvalue = datetime.date.min
                    else:
                         if (types_li[i].startswith("TIMESTAMP")):
                            initvalue = datetime.datetime.min
                globals[variables_li[i]] = initvalue
                i += 1
            # open file in read mode
            if (Import.expandedfilename is not None):
                if (Import.reader is None):
                    read_obj = open(Import.expandedfilename, 'r')
                    print(f">>>>>>>>> Importing from {Import.expandedfilename}")
                    if (stat(Import.expandedfilename).st_size == 0):
                        print("Import file is empty")
                        return
                    else:
                        # pass the file object to reader() to get the reader object
                        Import.reader = csv.reader(read_obj)
                # read next row
                print("Reading row")
                row = next(Import.reader)
                # row variable is a list that represents a row in csv
                i = 0
                while i < len(variables_li):
                    globals[variables_li[i]] = row[i]
                    i += 1
        except StopIteration:
            Import.no_more_rows = True
            print ("No more rows")
        except Exception as e:
            print (f"*** Failure importing {e}")
        print("Done importing")
    def reset():
            Import.expandedfilename = None
            Import.separator = ' '

Import.file = staticmethod(Import.file)
Import.using = staticmethod(Import.using)    

class Export:
    expandedfilename=None
    separator=' '
    def report(file, separator=' '):
        Export.separator = separator
        Export.expandedfilename = path.expandvars(file)
## obsolete
    def title_dashes(state="ON",withValue=None):
        pass
## obsolete
    def width(width):
        pass
## resets any previous export settings    
    def reset():
        Export.expandedfilename = None
        Export.separator = ' '

Export.title_dashes = staticmethod(Export.title_dashes)
Export.reset = staticmethod(Export.reset)
Export.report = staticmethod(Export.report)
Export.width = staticmethod(Export.width)

class Parameters:
    passed_variables = {}

## Loading extra parameters from command line
passed_variables = read_param_args(sys.argv[1:])
