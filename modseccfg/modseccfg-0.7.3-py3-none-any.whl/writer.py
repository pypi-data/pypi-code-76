# encoding: utf-8
# api: modseccfg
# title: Writer
# description: updates *.conf files with new directives
# version: 0.7
# type: file
# category: config
# config:
#     { name: write_etc, type: bool, value: 0, description: "Write to /etc without extra warnings", help: "Normally modseccfg would not update default apache/modsecurity config files." }
#     { name: write_sudo, type: bool, value: 0, description: "Use sudo to update non-writable files", help: "Run `sudo` on commandline to update files, if permissions insufficient" }
#     { name: backup_files, value: 1, type: bool, description: "Copy files to ~/backup-config/ before rewriting" }
#     { name: backup_dir, value: "~/backup-config/", type: str, description: "Where to store copies of configuration files" }
# state: alpha
#
# Reads, updates and then writes back configuration files.
# Contains multiple functions for different directives.
# Some need replacing, while others (lists) just need to be
# appended.
# 


import os, re, time, shutil
from modseccfg import vhosts, utils, recipe
from modseccfg.utils import srvroot, conf, log
import PySimpleGUI as sg


class rx:
    pfx = re.compile(r"""
        ^(\h*)\w+
    """, re.X|re.M)
    end = re.compile(r"""
        ^(?=\s*</VirtualHost>) | \Z
    """, re.X|re.M)
    end_preconf = re.compile(r"""
        ^(?=\s*</(Directory|VirtualHost)>) | \Z
    """, re.X|re.M)
    comments = re.compile("^\s*#.+", re.M)
    preconf_directives = re.compile(r"""
       ctl:removeBy\w+= | ctl:disable\w+= | ctl:ruleEngine= | ctl:auditEngine= | ^\h*Use\h*Sec\w+
    """, re.X|re.M)


#-- file I/O --

# read src from config file
def read(fn):
    return srvroot.read(fn)

# update file
def write(fn, src):
    is_system_file = re.search("^/etc/|^/usr/share/", fn) and not re.search("/sites-enabled/|/crs-setup.conf|RE\w+-\d+-EXCLUSION", fn)
    if is_system_file and not conf.write_etc:
        # alternatively check for `#editable:1` header with pluginconf
        if sg.popup_yes_no(f"Default Apache/mod_sec config file '{fn}' should not be updated. Proceed anyway?") != "Yes":
            return
    if not srvroot.writable(fn):
        sg.popup_cancel(f"Config file '{fn}' isn't writeable. (Use chown/chmod to make it so.)")
        # elif conf.write_sudo: write_sudo(fn, src)
        return
    # save a copy before doing anything else
    if conf.backup_files:
        backup(fn)
    # actually write
    srvroot.write(fn, src)

# copy *.conf to ~/backup-config/
def backup(fn):
    dir = utils.expandpath(conf.backup_dir)
    os.makedirs(dir, 0o751, True)
    dest = re.sub("[^\w\.\-\+\,]", "_", fn)
    dest = f"{dir}/{time.time()}.{dest}"
    shutil.copyfile(srvroot.fn(fn), dest)

# write to file via sudo/tee pipe instead
def write_sudo(fn, src):
    p = subprocess.Popen(['sudo', 'tee'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(src.encode("utf-8"))
    p.stdin.close()
    print(p.stdout.read())
    p.wait()


# detect if changes should go to vhost.*.preconf
# this will probably just be used by recipes to swap out the target filename
def fn_preconf(fn, addsrc, force_preconf=False, create=True):
    # test if we should act at all
    if force_preconf:
        pass
    elif not rx.preconf_directive.search(rx.comments.sub("", addsrc)):
        return fn
    elif not conf.get("preconf"):
        return fn
    elif not vhosts.tmp.decl_preconf:
        log.writer.warn("*.preconf includes don't seem to be configured.")
    # create
    new_fn = re.sub("\.(preconf|conf|dir|cfg|inc|load|vhost)$", ".preconf", fn)
    if not new_fn.endswith(".preconf") and fn == new_fn:
        new_fn += ".preconf"
    if create and not srvroot.exists(newfn):
        log.writer.info("Creating new preconf stub", new_fn) 
        vh = vhosts.vhost.get(fn)
        if vh and vh.name:
            src = recipe.templates.Setup["preconf_stub"]
            src = src.format({
                "DocumentRoot": vh.cfg.get("documentroot", f"/www/{vh.name}/"),
                "ServerName": vh.name
            })
            srvroot.write(new_fn, src)
    return new_fn

# use either rx.end or rx.end_preconf (looking for </Dir> instead of </VH)
def rx_end_preconf(fn):
    if fn.endswith(".preconf"):
        return rx.end_preconf
    else:
        return rx.end

# detect leading whitespace
def pfx(src):
    space = rx.pfx.findall(src)
    if space:
        return space[0]
    else:
        return ""
# add leading space to all lines of insert block
def prepend_pfx(add, pfx=""):
    if pfx:
        add = re.sub("^", pfx, add, re.M)
    return add

#-- update methods --

# directive insertion doesn't look for context
def append(fn, directive, value, comment=""):
    src = read(fn)
    insert = f"{directive} {value}   {comment}\n"
    insert = prepend_pfx(insert, pfx(src))
    rx_end = rx_end_preconf(fn)
    srcnew = rx_end.sub(insert, src, 1)
    write(fn, srcnew)        # count ↑ =0 would insert before all </VirtualHost> markers

# strip SecRuleRemoveById …? nnnnnnn …?
def remove_remove(fn, directive, value):
    src = read(fn)
    variants = {
        rf"^\s* {directive} \s+ {value} \s* (\#.*)?$": r'',
        rf"^ ( \s*{directive} \s+ (?:\d+\s+)+ ) \b{value}\b ( .* )$": r'\1\2'
    }
    for rx,repl in variants.items():
        if re.search(rx, src, re.X|re.M|re.I):
            src = re.sub(rx, repl, src, 1, re.X|re.M|re.I)
            return write(fn, src)
    print("NOT FOUND / NO CHANGES")

# list of SecOptions to be added/changed
def update_or_add(fn, pairs):
    src = read(fn)
    spc = pfx(src)
    for dir,val in pairs.items():
        # dir=regex
        if type(dir) is re.Pattern:
            if re.search(dir, src):
                src = re.sub(dir, val, src, 1)
            else:
                src = src + val
        # StringDirective
        elif re.search(rf"^[\ \t]*({dir}\b)", src, re.M|re.I):
            src = re.sub(rf"^([\ \t]*)({dir}\b).+\n", f"\\1{dir} {val}\n", src, 1, re.M|re.I)
        else:
            src = src + f"{spc}{dir} {val}\n"
    write(fn, src)

