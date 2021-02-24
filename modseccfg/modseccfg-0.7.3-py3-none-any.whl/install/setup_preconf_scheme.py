# api: modseccfg
# title: set up *.preconf
# description:
# type: internal
# category: install
# version: 0.1
#
# Basically just invokes the according recipe, after selecting
# 900-EXCLUSION as vhost, and updates `conf.preconf` setting.


import re
from modseccfg import vhosts, recipe, utils, writer
from modseccfg.utils import conf, log

# find target .conf
confn = ""
for fn in vhosts.vhosts.keys():
    if re.search("900-EXCLUSION", fn):
        confn = fn
if not confn:
    print("Couldn't find 900-EXCLUSION.conf")
else:

    # run recipe window
    if vhosts.tmp.decl_preconf:
        print("🗸 *.preconf includes already configured")
    else:
        print("\n# IncludeOptional .../*.preconf")
        src = recipe.template_funcs.crs_preconfig(vars={}, data={"confn":confn})
        writer.append(fn=confn, directive=src, value="", comment="")
        vhosts.tmp.decl_preconf = True
        print(f"→ updated: {confn}")

    # conf.preconf
    if conf.preconf:
        print("🗸 preconf use already activated")
    else:
        print("# enable 🗹 preconf usage globally")
        utils.conf.preconf = True
        utils.cfg_write()
        print(f"→ updated: {conf.conf_dir}/{conf.conf_file}")

