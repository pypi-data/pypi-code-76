import enum
from datetime import datetime
from pathlib import Path
from typing import Dict

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import Index

from lilili import __title__

DB_PATH = "sqlite:///" + str(Path.cwd() / f"{__title__}.sqlite3")
engine = create_engine(DB_PATH, echo=False)
Base = declarative_base()


class Basis(enum.Enum):
    """Basis for licensing decisions."""

    API_EXACT = 1
    API_LATEST = 2
    GITHUB_LICENSES_API = 3
    GITHUB_OTHER = 4


class Spdx(enum.Enum):
    """The SPDX license list.

    See Also
    --------
    https://spdx.org/licenses/
    """

    # value = (SPDX id, SPDX name, aliases... )
    _0BSD = ("0BSD", "BSD Zero Clause License")
    AAL = ("AAL", "Attribution Assurance License")
    ADSL = ("ADSL", "Amazon Digital Services License")
    AFL_11 = ("AFL-1.1", "Academic Free License v1.1")
    AFL_12 = ("AFL-1.2", "Academic Free License v1.2")
    AFL_20 = ("AFL-2.0", "Academic Free License v2.0")
    AFL_21 = ("AFL-2.1", "Academic Free License v2.1")
    AFL_30 = ("AFL-3.0", "Academic Free License v3.0")
    AGPL_10 = ("AGPL-1.0", "Affero General Public License v1.0")
    AGPL_10_ONLY = ("AGPL-1.0-only", "Affero General Public License v1.0 only")
    AGPL_10_OR_LATER = (
        "AGPL-1.0-or-later",
        "Affero General Public License v1.0 or later",
    )
    AGPL_30 = ("AGPL-3.0", "GNU Affero General Public License v3.0")
    AGPL_30_ONLY = ("AGPL-3.0-only", "GNU Affero General Public License v3.0 only")
    AGPL_30_OR_LATER = (
        "AGPL-3.0-or-later",
        "GNU Affero General Public License v3.0 or later",
    )
    AMDPLPA = ("AMDPLPA", "AMD's plpa_map.c License")
    AML = ("AML", "Apple MIT License")
    AMPAS = ("AMPAS", "Academy of Motion Picture Arts and Sciences BSD")
    ANTLR_PD = ("ANTLR-PD", "ANTLR Software Rights Notice")
    ANTLR_PD_FALLBACK = (
        "ANTLR-PD-fallback",
        "ANTLR Software Rights Notice with license fallback",
    )
    APAFML = ("APAFML", "Adobe Postscript AFM License")
    APL_10 = ("APL-1.0", "Adaptive Public License 1.0")
    APSL_10 = ("APSL-1.0", "Apple Public Source License 1.0")
    APSL_11 = ("APSL-1.1", "Apple Public Source License 1.1")
    APSL_12 = ("APSL-1.2", "Apple Public Source License 1.2")
    APSL_20 = ("APSL-2.0", "Apple Public Source License 2.0")
    ABSTYLES = ("Abstyles", "Abstyles License")
    ADOBE_2006 = (
        "Adobe-2006",
        "Adobe Systems Incorporated Source Code License Agreement",
    )
    ADOBE_GLYPH = ("Adobe-Glyph", "Adobe Glyph List License")
    AFMPARSE = ("Afmparse", "Afmparse License")
    ALADDIN = ("Aladdin", "Aladdin Free Public License")
    APACHE_10 = ("Apache-1.0", "Apache License 1.0")
    APACHE_11 = ("Apache-1.1", "Apache License 1.1")
    APACHE_20 = ("Apache-2.0", "Apache License 2.0")
    ARTISTIC_10 = ("Artistic-1.0", "Artistic License 1.0")
    ARTISTIC_10_PERL = ("Artistic-1.0-Perl", "Artistic License 1.0 (Perl)")
    ARTISTIC_10_CL8 = ("Artistic-1.0-cl8", "Artistic License 1.0 w/clause 8")
    ARTISTIC_20 = ("Artistic-2.0", "Artistic License 2.0")
    BSD_1_CLAUSE = ("BSD-1-Clause", "BSD 1-Clause License")
    BSD_2_CLAUSE = ("BSD-2-Clause", 'BSD 2-Clause "Simplified" License')
    BSD_2_CLAUSE_FREEBSD = ("BSD-2-Clause-FreeBSD", "BSD 2-Clause FreeBSD License")
    BSD_2_CLAUSE_NETBSD = ("BSD-2-Clause-NetBSD", "BSD 2-Clause NetBSD License")
    BSD_2_CLAUSE_PATENT = ("BSD-2-Clause-Patent", "BSD-2-Clause Plus Patent License")
    BSD_2_CLAUSE_VIEWS = ("BSD-2-Clause-Views", "BSD 2-Clause with views sentence")
    BSD_3_CLAUSE = ("BSD-3-Clause", 'BSD 3-Clause "New" or "Revised" License')
    BSD_3_CLAUSE_ATTRIBUTION = ("BSD-3-Clause-Attribution", "BSD with attribution")
    BSD_3_CLAUSE_CLEAR = ("BSD-3-Clause-Clear", "BSD 3-Clause Clear License")
    BSD_3_CLAUSE_LBNL = (
        "BSD-3-Clause-LBNL",
        "Lawrence Berkeley National Labs BSD variant license",
    )
    BSD_3_CLAUSE_NO_NUCLEAR_LICENSE = (
        "BSD-3-Clause-No-Nuclear-License",
        "BSD 3-Clause No Nuclear License",
    )
    BSD_3_CLAUSE_NO_NUCLEAR_LICENSE_2014 = (
        "BSD-3-Clause-No-Nuclear-License-2014",
        "BSD 3-Clause No Nuclear License 2014",
    )
    BSD_3_CLAUSE_NO_NUCLEAR_WARRANTY = (
        "BSD-3-Clause-No-Nuclear-Warranty",
        "BSD 3-Clause No Nuclear Warranty",
    )
    BSD_3_CLAUSE_OPEN_MPI = ("BSD-3-Clause-Open-MPI", "BSD 3-Clause Open MPI variant")
    BSD_4_CLAUSE = ("BSD-4-Clause", 'BSD 4-Clause "Original" or "Old" License')
    BSD_4_CLAUSE_SHORTENED = ("BSD-4-Clause-Shortened", "BSD 4 Clause Shortened")
    BSD_4_CLAUSE_UC = (
        "BSD-4-Clause-UC",
        "BSD-4-Clause (University of California-Specific)",
    )
    BSD_PROTECTION = ("BSD-Protection", "BSD Protection License")
    BSD_SOURCE_CODE = ("BSD-Source-Code", "BSD Source Code Attribution")
    BSL_10 = ("BSL-1.0", "Boost Software License 1.0")
    BUSL_11 = ("BUSL-1.1", "Business Source License 1.1")
    BAHYPH = ("Bahyph", "Bahyph License")
    BARR = ("Barr", "Barr License")
    BEERWARE = ("Beerware", "Beerware License")
    BITTORRENT_10 = ("BitTorrent-1.0", "BitTorrent Open Source License v1.0")
    BITTORRENT_11 = ("BitTorrent-1.1", "BitTorrent Open Source License v1.1")
    BLUEOAK_100 = ("BlueOak-1.0.0", "Blue Oak Model License 1.0.0")
    BORCEUX = ("Borceux", "Borceux license")
    CAL_10 = ("CAL-1.0", "Cryptographic Autonomy License 1.0")
    CAL_10_COMBINED_WORK_EXCEPTION = (
        "CAL-1.0-Combined-Work-Exception",
        "Cryptographic Autonomy License 1.0 (Combined Work Exception)",
    )
    CATOSL_11 = ("CATOSL-1.1", "Computer Associates Trusted Open Source License 1.1")
    CC_BY_10 = ("CC-BY-1.0", "Creative Commons Attribution 1.0 Generic")
    CC_BY_20 = ("CC-BY-2.0", "Creative Commons Attribution 2.0 Generic")
    CC_BY_25 = ("CC-BY-2.5", "Creative Commons Attribution 2.5 Generic")
    CC_BY_30 = ("CC-BY-3.0", "Creative Commons Attribution 3.0 Unported")
    CC_BY_30_AT = ("CC-BY-3.0-AT", "Creative Commons Attribution 3.0 Austria")
    CC_BY_30_US = ("CC-BY-3.0-US", "Creative Commons Attribution 3.0 United States")
    CC_BY_40 = ("CC-BY-4.0", "Creative Commons Attribution 4.0 International")
    CC_BY_NC_10 = (
        "CC-BY-NC-1.0",
        "Creative Commons Attribution Non Commercial 1.0 Generic",
    )
    CC_BY_NC_20 = (
        "CC-BY-NC-2.0",
        "Creative Commons Attribution Non Commercial 2.0 Generic",
    )
    CC_BY_NC_25 = (
        "CC-BY-NC-2.5",
        "Creative Commons Attribution Non Commercial 2.5 Generic",
    )
    CC_BY_NC_30 = (
        "CC-BY-NC-3.0",
        "Creative Commons Attribution Non Commercial 3.0 Unported",
    )
    CC_BY_NC_40 = (
        "CC-BY-NC-4.0",
        "Creative Commons Attribution Non Commercial 4.0 International",
    )
    CC_BY_NC_ND_10 = (
        "CC-BY-NC-ND-1.0",
        "Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic",
    )
    CC_BY_NC_ND_20 = (
        "CC-BY-NC-ND-2.0",
        "Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic",
    )
    CC_BY_NC_ND_25 = (
        "CC-BY-NC-ND-2.5",
        "Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic",
    )
    CC_BY_NC_ND_30 = (
        "CC-BY-NC-ND-3.0",
        "Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported",
    )
    CC_BY_NC_ND_30_IGO = (
        "CC-BY-NC-ND-3.0-IGO",
        "Creative Commons Attribution Non Commercial No Derivatives 3.0 IGO",
    )
    CC_BY_NC_ND_40 = (
        "CC-BY-NC-ND-4.0",
        "Creative Commons Attribution Non Commercial No Derivatives 4.0 International",
    )
    CC_BY_NC_SA_10 = (
        "CC-BY-NC-SA-1.0",
        "Creative Commons Attribution Non Commercial Share Alike 1.0 Generic",
    )
    CC_BY_NC_SA_20 = (
        "CC-BY-NC-SA-2.0",
        "Creative Commons Attribution Non Commercial Share Alike 2.0 Generic",
    )
    CC_BY_NC_SA_25 = (
        "CC-BY-NC-SA-2.5",
        "Creative Commons Attribution Non Commercial Share Alike 2.5 Generic",
    )
    CC_BY_NC_SA_30 = (
        "CC-BY-NC-SA-3.0",
        "Creative Commons Attribution Non Commercial Share Alike 3.0 Unported",
    )
    CC_BY_NC_SA_40 = (
        "CC-BY-NC-SA-4.0",
        "Creative Commons Attribution Non Commercial Share Alike 4.0 International",
    )
    CC_BY_ND_10 = (
        "CC-BY-ND-1.0",
        "Creative Commons Attribution No Derivatives 1.0 Generic",
    )
    CC_BY_ND_20 = (
        "CC-BY-ND-2.0",
        "Creative Commons Attribution No Derivatives 2.0 Generic",
    )
    CC_BY_ND_25 = (
        "CC-BY-ND-2.5",
        "Creative Commons Attribution No Derivatives 2.5 Generic",
    )
    CC_BY_ND_30 = (
        "CC-BY-ND-3.0",
        "Creative Commons Attribution No Derivatives 3.0 Unported",
    )
    CC_BY_ND_40 = (
        "CC-BY-ND-4.0",
        "Creative Commons Attribution No Derivatives 4.0 International",
    )
    CC_BY_SA_10 = (
        "CC-BY-SA-1.0",
        "Creative Commons Attribution Share Alike 1.0 Generic",
    )
    CC_BY_SA_20 = (
        "CC-BY-SA-2.0",
        "Creative Commons Attribution Share Alike 2.0 Generic",
    )
    CC_BY_SA_20_UK = (
        "CC-BY-SA-2.0-UK",
        "Creative Commons Attribution Share Alike 2.0 England and Wales",
    )
    CC_BY_SA_25 = (
        "CC-BY-SA-2.5",
        "Creative Commons Attribution Share Alike 2.5 Generic",
    )
    CC_BY_SA_30 = (
        "CC-BY-SA-3.0",
        "Creative Commons Attribution Share Alike 3.0 Unported",
    )
    CC_BY_SA_30_AT = (
        "CC-BY-SA-3.0-AT",
        "Creative Commons Attribution-Share Alike 3.0 Austria",
    )
    CC_BY_SA_40 = (
        "CC-BY-SA-4.0",
        "Creative Commons Attribution Share Alike 4.0 International",
    )
    CC_PDDC = ("CC-PDDC", "Creative Commons Public Domain Dedication and Certification")
    CC0_10 = ("CC0-1.0", "Creative Commons Zero v1.0 Universal")
    CDDL_10 = ("CDDL-1.0", "Common Development and Distribution License 1.0")
    CDDL_11 = ("CDDL-1.1", "Common Development and Distribution License 1.1")
    CDLA_PERMISSIVE_10 = (
        "CDLA-Permissive-1.0",
        "Community Data License Agreement Permissive 1.0",
    )
    CDLA_SHARING_10 = (
        "CDLA-Sharing-1.0",
        "Community Data License Agreement Sharing 1.0",
    )
    CECILL_10 = ("CECILL-1.0", "CeCILL Free Software License Agreement v1.0")
    CECILL_11 = ("CECILL-1.1", "CeCILL Free Software License Agreement v1.1")
    CECILL_20 = ("CECILL-2.0", "CeCILL Free Software License Agreement v2.0")
    CECILL_21 = ("CECILL-2.1", "CeCILL Free Software License Agreement v2.1")
    CECILL_B = ("CECILL-B", "CeCILL-B Free Software License Agreement")
    CECILL_C = ("CECILL-C", "CeCILL-C Free Software License Agreement")
    CERN_OHL_11 = ("CERN-OHL-1.1", "CERN Open Hardware Licence v1.1")
    CERN_OHL_12 = ("CERN-OHL-1.2", "CERN Open Hardware Licence v1.2")
    CERN_OHL_P_20 = (
        "CERN-OHL-P-2.0",
        "CERN Open Hardware Licence Version 2 - Permissive",
    )
    CERN_OHL_S_20 = (
        "CERN-OHL-S-2.0",
        "CERN Open Hardware Licence Version 2 - Strongly Reciprocal",
    )
    CERN_OHL_W_20 = (
        "CERN-OHL-W-2.0",
        "CERN Open Hardware Licence Version 2 - Weakly Reciprocal",
    )
    CNRI_JYTHON = ("CNRI-Jython", "CNRI Jython License")
    CNRI_PYTHON = ("CNRI-Python", "CNRI Python License")
    CNRI_PYTHON_GPL_COMPATIBLE = (
        "CNRI-Python-GPL-Compatible",
        "CNRI Python Open Source GPL Compatible License Agreement",
    )
    CPAL_10 = ("CPAL-1.0", "Common Public Attribution License 1.0")
    CPL_10 = ("CPL-1.0", "Common Public License 1.0")
    CPOL_102 = ("CPOL-1.02", "Code Project Open License 1.02")
    CUA_OPL_10 = ("CUA-OPL-1.0", "CUA Office Public License v1.0")
    CALDERA = ("Caldera", "Caldera License")
    CLARTISTIC = ("ClArtistic", "Clarified Artistic License")
    CONDOR_11 = ("Condor-1.1", "Condor Public License v1.1")
    CROSSWORD = ("Crossword", "Crossword License")
    CRYSTALSTACKER = ("CrystalStacker", "CrystalStacker License")
    CUBE = ("Cube", "Cube License")
    D_FSL_10 = ("D-FSL-1.0", "Deutsche Freie Software Lizenz")
    DOC = ("DOC", "DOC License")
    DRL_10 = ("DRL-1.0", "Detection Rule License 1.0")
    DSDP = ("DSDP", "DSDP License")
    DOTSEQN = ("Dotseqn", "Dotseqn License")
    ECL_10 = ("ECL-1.0", "Educational Community License v1.0")
    ECL_20 = ("ECL-2.0", "Educational Community License v2.0")
    EFL_10 = ("EFL-1.0", "Eiffel Forum License v1.0")
    EFL_20 = ("EFL-2.0", "Eiffel Forum License v2.0")
    EPICS = ("EPICS", "EPICS Open License")
    EPL_10 = ("EPL-1.0", "Eclipse Public License 1.0")
    EPL_20 = ("EPL-2.0", "Eclipse Public License 2.0")
    EUDATAGRID = ("EUDatagrid", "EU DataGrid Software License")
    EUPL_10 = ("EUPL-1.0", "European Union Public License 1.0")
    EUPL_11 = ("EUPL-1.1", "European Union Public License 1.1")
    EUPL_12 = ("EUPL-1.2", "European Union Public License 1.2")
    ENTESSA = ("Entessa", "Entessa Public License v1.0")
    ERLPL_11 = ("ErlPL-1.1", "Erlang Public License v1.1")
    EUROSYM = ("Eurosym", "Eurosym License")
    FSFAP = ("FSFAP", "FSF All Permissive License")
    FSFUL = ("FSFUL", "FSF Unlimited License")
    FSFULLR = ("FSFULLR", "FSF Unlimited License (with License Retention)")
    FTL = ("FTL", "Freetype Project License")
    FAIR = ("Fair", "Fair License")
    FRAMEWORX_10 = ("Frameworx-1.0", "Frameworx Open License 1.0")
    FREEBSD_DOC = ("FreeBSD-DOC", "FreeBSD Documentation License")
    FREEIMAGE = ("FreeImage", "FreeImage Public License v1.0")
    GFDL_11 = ("GFDL-1.1", "GNU Free Documentation License v1.1")
    GFDL_11_INVARIANTS_ONLY = (
        "GFDL-1.1-invariants-only",
        "GNU Free Documentation License v1.1 only - invariants",
    )
    GFDL_11_INVARIANTS_OR_LATER = (
        "GFDL-1.1-invariants-or-later",
        "GNU Free Documentation License v1.1 or later - invariants",
    )
    GFDL_11_NO_INVARIANTS_ONLY = (
        "GFDL-1.1-no-invariants-only",
        "GNU Free Documentation License v1.1 only - no invariants",
    )
    GFDL_11_NO_INVARIANTS_OR_LATER = (
        "GFDL-1.1-no-invariants-or-later",
        "GNU Free Documentation License v1.1 or later - no invariants",
    )
    GFDL_11_ONLY = ("GFDL-1.1-only", "GNU Free Documentation License v1.1 only")
    GFDL_11_OR_LATER = (
        "GFDL-1.1-or-later",
        "GNU Free Documentation License v1.1 or later",
    )
    GFDL_12 = ("GFDL-1.2", "GNU Free Documentation License v1.2")
    GFDL_12_INVARIANTS_ONLY = (
        "GFDL-1.2-invariants-only",
        "GNU Free Documentation License v1.2 only - invariants",
    )
    GFDL_12_INVARIANTS_OR_LATER = (
        "GFDL-1.2-invariants-or-later",
        "GNU Free Documentation License v1.2 or later - invariants",
    )
    GFDL_12_NO_INVARIANTS_ONLY = (
        "GFDL-1.2-no-invariants-only",
        "GNU Free Documentation License v1.2 only - no invariants",
    )
    GFDL_12_NO_INVARIANTS_OR_LATER = (
        "GFDL-1.2-no-invariants-or-later",
        "GNU Free Documentation License v1.2 or later - no invariants",
    )
    GFDL_12_ONLY = ("GFDL-1.2-only", "GNU Free Documentation License v1.2 only")
    GFDL_12_OR_LATER = (
        "GFDL-1.2-or-later",
        "GNU Free Documentation License v1.2 or later",
    )
    GFDL_13 = ("GFDL-1.3", "GNU Free Documentation License v1.3")
    GFDL_13_INVARIANTS_ONLY = (
        "GFDL-1.3-invariants-only",
        "GNU Free Documentation License v1.3 only - invariants",
    )
    GFDL_13_INVARIANTS_OR_LATER = (
        "GFDL-1.3-invariants-or-later",
        "GNU Free Documentation License v1.3 or later - invariants",
    )
    GFDL_13_NO_INVARIANTS_ONLY = (
        "GFDL-1.3-no-invariants-only",
        "GNU Free Documentation License v1.3 only - no invariants",
    )
    GFDL_13_NO_INVARIANTS_OR_LATER = (
        "GFDL-1.3-no-invariants-or-later",
        "GNU Free Documentation License v1.3 or later - no invariants",
    )
    GFDL_13_ONLY = ("GFDL-1.3-only", "GNU Free Documentation License v1.3 only")
    GFDL_13_OR_LATER = (
        "GFDL-1.3-or-later",
        "GNU Free Documentation License v1.3 or later",
    )
    GL2PS = ("GL2PS", "GL2PS License")
    GLWTPL = ("GLWTPL", "Good Luck With That Public License")
    GPL_10 = ("GPL-1.0", "GNU General Public License v1.0 only")
    GPL_10p = ("GPL-1.0+", "GNU General Public License v1.0 or later")
    GPL_10_ONLY = ("GPL-1.0-only", "GNU General Public License v1.0 only")
    GPL_10_OR_LATER = ("GPL-1.0-or-later", "GNU General Public License v1.0 or later")
    GPL_20 = ("GPL-2.0", "GNU General Public License v2.0 only")
    GPL_20p = ("GPL-2.0+", "GNU General Public License v2.0 or later")
    GPL_20_ONLY = ("GPL-2.0-only", "GNU General Public License v2.0 only")
    GPL_20_OR_LATER = ("GPL-2.0-or-later", "GNU General Public License v2.0 or later")
    GPL_20_WITH_GCC_EXCEPTION = (
        "GPL-2.0-with-GCC-exception",
        "GNU General Public License v2.0 w/GCC Runtime Library exception",
    )
    GPL_20_WITH_AUTOCONF_EXCEPTION = (
        "GPL-2.0-with-autoconf-exception",
        "GNU General Public License v2.0 w/Autoconf exception",
    )
    GPL_20_WITH_BISON_EXCEPTION = (
        "GPL-2.0-with-bison-exception",
        "GNU General Public License v2.0 w/Bison exception",
    )
    GPL_20_WITH_CLASSPATH_EXCEPTION = (
        "GPL-2.0-with-classpath-exception",
        "GNU General Public License v2.0 w/Classpath exception",
    )
    GPL_20_WITH_FONT_EXCEPTION = (
        "GPL-2.0-with-font-exception",
        "GNU General Public License v2.0 w/Font exception",
    )
    GPL_30 = ("GPL-3.0", "GNU General Public License v3.0 only")
    GPL_30p = ("GPL-3.0+", "GNU General Public License v3.0 or later")
    GPL_30_ONLY = ("GPL-3.0-only", "GNU General Public License v3.0 only")
    GPL_30_OR_LATER = ("GPL-3.0-or-later", "GNU General Public License v3.0 or later")
    GPL_30_WITH_GCC_EXCEPTION = (
        "GPL-3.0-with-GCC-exception",
        "GNU General Public License v3.0 w/GCC Runtime Library exception",
    )
    GPL_30_WITH_AUTOCONF_EXCEPTION = (
        "GPL-3.0-with-autoconf-exception",
        "GNU General Public License v3.0 w/Autoconf exception",
    )
    GIFTWARE = ("Giftware", "Giftware License")
    GLIDE = ("Glide", "3dfx Glide License")
    GLULXE = ("Glulxe", "Glulxe License")
    HPND = ("HPND", "Historical Permission Notice and Disclaimer")
    HPND_SELL_VARIANT = (
        "HPND-sell-variant",
        "Historical Permission Notice and Disclaimer - sell variant",
    )
    HTMLTIDY = ("HTMLTIDY", "HTML Tidy License")
    HASKELLREPORT = ("HaskellReport", "Haskell Language Report License")
    HIPPOCRATIC_21 = ("Hippocratic-2.1", "Hippocratic License 2.1")
    IBM_PIBS = ("IBM-pibs", "IBM PowerPC Initialization and Boot Software")
    ICU = ("ICU", "ICU License")
    IJG = ("IJG", "Independent JPEG Group License")
    IPA = ("IPA", "IPA Font License")
    IPL_10 = ("IPL-1.0", "IBM Public License v1.0")
    ISC = ("ISC", "ISC License")
    IMAGEMAGICK = ("ImageMagick", "ImageMagick License")
    IMLIB2 = ("Imlib2", "Imlib2 License")
    INFO_ZIP = ("Info-ZIP", "Info-ZIP License")
    INTEL = ("Intel", "Intel Open Source License")
    INTEL_ACPI = ("Intel-ACPI", "Intel ACPI Software License Agreement")
    INTERBASE_10 = ("Interbase-1.0", "Interbase Public License v1.0")
    JPNIC = ("JPNIC", "Japan Network Information Center License")
    JSON = ("JSON", "JSON License")
    JASPER_20 = ("JasPer-2.0", "JasPer License")
    LAL_12 = ("LAL-1.2", "Licence Art Libre 1.2")
    LAL_13 = ("LAL-1.3", "Licence Art Libre 1.3")
    LGPL_20 = ("LGPL-2.0", "GNU Library General Public License v2 only")
    LGPL_20p = ("LGPL-2.0+", "GNU Library General Public License v2 or later")
    LGPL_20_ONLY = ("LGPL-2.0-only", "GNU Library General Public License v2 only")
    LGPL_20_OR_LATER = (
        "LGPL-2.0-or-later",
        "GNU Library General Public License v2 or later",
    )
    LGPL_21 = ("LGPL-2.1", "GNU Lesser General Public License v2.1 only")
    LGPL_21p = ("LGPL-2.1+", "GNU Library General Public License v2.1 or later")
    LGPL_21_ONLY = ("LGPL-2.1-only", "GNU Lesser General Public License v2.1 only")
    LGPL_21_OR_LATER = (
        "LGPL-2.1-or-later",
        "GNU Lesser General Public License v2.1 or later",
    )
    LGPL_30 = ("LGPL-3.0", "GNU Lesser General Public License v3.0 only")
    LGPL_30p = ("LGPL-3.0+", "GNU Lesser General Public License v3.0 or later")
    LGPL_30_ONLY = ("LGPL-3.0-only", "GNU Lesser General Public License v3.0 only")
    LGPL_30_OR_LATER = (
        "LGPL-3.0-or-later",
        "GNU Lesser General Public License v3.0 or later",
    )
    LGPLLR = ("LGPLLR", "Lesser General Public License For Linguistic Resources")
    LPL_10 = ("LPL-1.0", "Lucent Public License Version 1.0")
    LPL_102 = ("LPL-1.02", "Lucent Public License v1.02")
    LPPL_10 = ("LPPL-1.0", "LaTeX Project Public License v1.0")
    LPPL_11 = ("LPPL-1.1", "LaTeX Project Public License v1.1")
    LPPL_12 = ("LPPL-1.2", "LaTeX Project Public License v1.2")
    LPPL_13A = ("LPPL-1.3a", "LaTeX Project Public License v1.3a")
    LPPL_13C = ("LPPL-1.3c", "LaTeX Project Public License v1.3c")
    LATEX2E = ("Latex2e", "Latex2e License")
    LEPTONICA = ("Leptonica", "Leptonica License")
    LILIQ_P_11 = ("LiLiQ-P-1.1", "Licence Libre du Québec – Permissive version 1.1")
    LILIQ_R_11 = ("LiLiQ-R-1.1", "Licence Libre du Québec – Réciprocité version 1.1")
    LILIQ_RPLUS_11 = (
        "LiLiQ-Rplus-1.1",
        "Licence Libre du Québec – Réciprocité forte version 1.1",
    )
    LIBPNG = ("Libpng", "libpng License")
    LINUX_OPENIB = ("Linux-OpenIB", "Linux Kernel Variant of OpenIB.org license")
    MIT = ("MIT", "MIT License", "The MIT License")
    MIT_0 = ("MIT-0", "MIT No Attribution")
    MIT_CMU = ("MIT-CMU", "CMU License")
    MIT_ADVERTISING = ("MIT-advertising", "Enlightenment License (e16)")
    MIT_ENNA = ("MIT-enna", "enna License")
    MIT_FEH = ("MIT-feh", "feh License")
    MIT_OPEN_GROUP = ("MIT-open-group", "MIT Open Group variant")
    MITNFA = ("MITNFA", "MIT +no-false-attribs license")
    MPL_10 = ("MPL-1.0", "Mozilla Public License 1.0")
    MPL_11 = ("MPL-1.1", "Mozilla Public License 1.1")
    MPL_20 = ("MPL-2.0", "Mozilla Public License 2.0")
    MPL_20_NO_COPYLEFT_EXCEPTION = (
        "MPL-2.0-no-copyleft-exception",
        "Mozilla Public License 2.0 (no copyleft exception)",
    )
    MS_PL = ("MS-PL", "Microsoft Public License")
    MS_RL = ("MS-RL", "Microsoft Reciprocal License")
    MTLL = ("MTLL", "Matrix Template Library License")
    MAKEINDEX = ("MakeIndex", "MakeIndex License")
    MIROS = ("MirOS", "The MirOS Licence")
    MOTOSOTO = ("Motosoto", "Motosoto License")
    MULANPSL_10 = ("MulanPSL-1.0", "Mulan Permissive Software License, Version 1")
    MULANPSL_20 = ("MulanPSL-2.0", "Mulan Permissive Software License, Version 2")
    MULTICS = ("Multics", "Multics License")
    MUP = ("Mup", "Mup License")
    NASA_13 = ("NASA-1.3", "NASA Open Source Agreement 1.3")
    NBPL_10 = ("NBPL-1.0", "Net Boolean Public License v1")
    NCGL_UK_20 = ("NCGL-UK-2.0", "Non-Commercial Government Licence")
    NCSA = ("NCSA", "University of Illinois/NCSA Open Source License")
    NGPL = ("NGPL", "Nethack General Public License")
    NIST_PD = ("NIST-PD", "NIST Public Domain Notice")
    NIST_PD_FALLBACK = (
        "NIST-PD-fallback",
        "NIST Public Domain Notice with license fallback",
    )
    NLOD_10 = ("NLOD-1.0", "Norwegian Licence for Open Government Data")
    NLPL = ("NLPL", "No Limit Public License")
    NOSL = ("NOSL", "Netizen Open Source License")
    NPL_10 = ("NPL-1.0", "Netscape Public License v1.0")
    NPL_11 = ("NPL-1.1", "Netscape Public License v1.1")
    NPOSL_30 = ("NPOSL-3.0", "Non-Profit Open Software License 3.0")
    NRL = ("NRL", "NRL License")
    NTP = ("NTP", "NTP License")
    NTP_0 = ("NTP-0", "NTP No Attribution")
    NAUMEN = ("Naumen", "Naumen Public License")
    NET_SNMP = ("Net-SNMP", "Net-SNMP License")
    NETCDF = ("NetCDF", "NetCDF license")
    NEWSLETR = ("Newsletr", "Newsletr License")
    NOKIA = ("Nokia", "Nokia Open Source License")
    NOWEB = ("Noweb", "Noweb License")
    NUNIT = ("Nunit", "Nunit License")
    O_UDA_10 = ("O-UDA-1.0", "Open Use of Data Agreement v1.0")
    OCCT_PL = ("OCCT-PL", "Open CASCADE Technology Public License")
    OCLC_20 = ("OCLC-2.0", "OCLC Research Public License 2.0")
    ODC_BY_10 = ("ODC-By-1.0", "Open Data Commons Attribution License v1.0")
    ODBL_10 = ("ODbL-1.0", "Open Data Commons Open Database License v1.0")
    OFL_10 = ("OFL-1.0", "SIL Open Font License 1.0")
    OFL_10_RFN = ("OFL-1.0-RFN", "SIL Open Font License 1.0 with Reserved Font Name")
    OFL_10_NO_RFN = (
        "OFL-1.0-no-RFN",
        "SIL Open Font License 1.0 with no Reserved Font Name",
    )
    OFL_11 = ("OFL-1.1", "SIL Open Font License 1.1")
    OFL_11_RFN = ("OFL-1.1-RFN", "SIL Open Font License 1.1 with Reserved Font Name")
    OFL_11_NO_RFN = (
        "OFL-1.1-no-RFN",
        "SIL Open Font License 1.1 with no Reserved Font Name",
    )
    OGC_10 = ("OGC-1.0", "OGC Software License, Version 1.0")
    OGL_CANADA_20 = ("OGL-Canada-2.0", "Open Government Licence - Canada")
    OGL_UK_10 = ("OGL-UK-1.0", "Open Government Licence v1.0")
    OGL_UK_20 = ("OGL-UK-2.0", "Open Government Licence v2.0")
    OGL_UK_30 = ("OGL-UK-3.0", "Open Government Licence v3.0")
    OGTSL = ("OGTSL", "Open Group Test Suite License")
    OLDAP_11 = ("OLDAP-1.1", "Open LDAP Public License v1.1")
    OLDAP_12 = ("OLDAP-1.2", "Open LDAP Public License v1.2")
    OLDAP_13 = ("OLDAP-1.3", "Open LDAP Public License v1.3")
    OLDAP_14 = ("OLDAP-1.4", "Open LDAP Public License v1.4")
    OLDAP_20 = (
        "OLDAP-2.0",
        "Open LDAP Public License v2.0 (or possibly 2.0A and 2.0B)",
    )
    OLDAP_201 = ("OLDAP-2.0.1", "Open LDAP Public License v2.0.1")
    OLDAP_21 = ("OLDAP-2.1", "Open LDAP Public License v2.1")
    OLDAP_22 = ("OLDAP-2.2", "Open LDAP Public License v2.2")
    OLDAP_221 = ("OLDAP-2.2.1", "Open LDAP Public License v2.2.1")
    OLDAP_222 = ("OLDAP-2.2.2", "Open LDAP Public License 2.2.2")
    OLDAP_23 = ("OLDAP-2.3", "Open LDAP Public License v2.3")
    OLDAP_24 = ("OLDAP-2.4", "Open LDAP Public License v2.4")
    OLDAP_25 = ("OLDAP-2.5", "Open LDAP Public License v2.5")
    OLDAP_26 = ("OLDAP-2.6", "Open LDAP Public License v2.6")
    OLDAP_27 = ("OLDAP-2.7", "Open LDAP Public License v2.7")
    OLDAP_28 = ("OLDAP-2.8", "Open LDAP Public License v2.8")
    OML = ("OML", "Open Market License")
    OPL_10 = ("OPL-1.0", "Open Public License v1.0")
    OSET_PL_21 = ("OSET-PL-2.1", "OSET Public License version 2.1")
    OSL_10 = ("OSL-1.0", "Open Software License 1.0")
    OSL_11 = ("OSL-1.1", "Open Software License 1.1")
    OSL_20 = ("OSL-2.0", "Open Software License 2.0")
    OSL_21 = ("OSL-2.1", "Open Software License 2.1")
    OSL_30 = ("OSL-3.0", "Open Software License 3.0")
    OPENSSL = ("OpenSSL", "OpenSSL License")
    PDDL_10 = ("PDDL-1.0", "Open Data Commons Public Domain Dedication & License 1.0")
    PHP_30 = ("PHP-3.0", "PHP License v3.0")
    PHP_301 = ("PHP-3.01", "PHP License v3.01")
    PSF_20 = ("PSF-2.0", "Python Software Foundation License 2.0")
    PARITY_600 = ("Parity-6.0.0", "The Parity Public License 6.0.0")
    PARITY_700 = ("Parity-7.0.0", "The Parity Public License 7.0.0")
    PLEXUS = ("Plexus", "Plexus Classworlds License")
    POLYFORM_NONCOMMERCIAL_100 = (
        "PolyForm-Noncommercial-1.0.0",
        "PolyForm Noncommercial License 1.0.0",
    )
    POLYFORM_SMALL_BUSINESS_100 = (
        "PolyForm-Small-Business-1.0.0",
        "PolyForm Small Business License 1.0.0",
    )
    POSTGRESQL = ("PostgreSQL", "PostgreSQL License")
    PYTHON_20 = ("Python-2.0", "Python License 2.0")
    QPL_10 = ("QPL-1.0", "Q Public License 1.0")
    QHULL = ("Qhull", "Qhull License")
    RHECOS_11 = ("RHeCos-1.1", "Red Hat eCos Public License v1.1")
    RPL_11 = ("RPL-1.1", "Reciprocal Public License 1.1")
    RPL_15 = ("RPL-1.5", "Reciprocal Public License 1.5")
    RPSL_10 = ("RPSL-1.0", "RealNetworks Public Source License v1.0")
    RSA_MD = ("RSA-MD", "RSA Message-Digest License")
    RSCPL = ("RSCPL", "Ricoh Source Code Public License")
    RDISC = ("Rdisc", "Rdisc License")
    RUBY = ("Ruby", "Ruby License")
    SAX_PD = ("SAX-PD", "Sax Public Domain Notice")
    SCEA = ("SCEA", "SCEA Shared Source License")
    SGI_B_10 = ("SGI-B-1.0", "SGI Free Software License B v1.0")
    SGI_B_11 = ("SGI-B-1.1", "SGI Free Software License B v1.1")
    SGI_B_20 = ("SGI-B-2.0", "SGI Free Software License B v2.0")
    SHL_05 = ("SHL-0.5", "Solderpad Hardware License v0.5")
    SHL_051 = ("SHL-0.51", "Solderpad Hardware License, Version 0.51")
    SISSL = ("SISSL", "Sun Industry Standards Source License v1.1")
    SISSL_12 = ("SISSL-1.2", "Sun Industry Standards Source License v1.2")
    SMLNJ = ("SMLNJ", "Standard ML of New Jersey License")
    SMPPL = ("SMPPL", "Secure Messaging Protocol Public License")
    SNIA = ("SNIA", "SNIA Public License 1.1")
    SPL_10 = ("SPL-1.0", "Sun Public License v1.0")
    SSH_OPENSSH = ("SSH-OpenSSH", "SSH OpenSSH license")
    SSH_SHORT = ("SSH-short", "SSH short notice")
    SSPL_10 = ("SSPL-1.0", "Server Side Public License, v 1")
    SWL = ("SWL", "Scheme Widget Library (SWL) Software License Agreement")
    SAXPATH = ("Saxpath", "Saxpath License")
    SENDMAIL = ("Sendmail", "Sendmail License")
    SENDMAIL_823 = ("Sendmail-8.23", "Sendmail License 8.23")
    SIMPL_20 = ("SimPL-2.0", "Simple Public License 2.0")
    SLEEPYCAT = ("Sleepycat", "Sleepycat License")
    SPENCER_86 = ("Spencer-86", "Spencer License 86")
    SPENCER_94 = ("Spencer-94", "Spencer License 94")
    SPENCER_99 = ("Spencer-99", "Spencer License 99")
    STANDARDML_NJ = ("StandardML-NJ", "Standard ML of New Jersey License")
    SUGARCRM_113 = ("SugarCRM-1.1.3", "SugarCRM Public License v1.1.3")
    TAPR_OHL_10 = ("TAPR-OHL-1.0", "TAPR Open Hardware License v1.0")
    TCL = ("TCL", "TCL/TK License")
    TCP_WRAPPERS = ("TCP-wrappers", "TCP Wrappers License")
    TMATE = ("TMate", "TMate Open Source License")
    TORQUE_11 = ("TORQUE-1.1", "TORQUE v2.5+ Software License v1.1")
    TOSL = ("TOSL", "Trusster Open Source License")
    TU_BERLIN_10 = ("TU-Berlin-1.0", "Technische Universitaet Berlin License 1.0")
    TU_BERLIN_20 = ("TU-Berlin-2.0", "Technische Universitaet Berlin License 2.0")
    UCL_10 = ("UCL-1.0", "Upstream Compatibility License v1.0")
    UPL_10 = ("UPL-1.0", "Universal Permissive License v1.0")
    UNICODE_DFS_2015 = (
        "Unicode-DFS-2015",
        "Unicode License Agreement - Data Files and Software (2015)",
    )
    UNICODE_DFS_2016 = (
        "Unicode-DFS-2016",
        "Unicode License Agreement - Data Files and Software (2016)",
    )
    UNICODE_TOU = ("Unicode-TOU", "Unicode Terms of Use")
    UNLICENSE = ("Unlicense", "The Unlicense")
    VOSTROM = ("VOSTROM", "VOSTROM Public License for Open Source")
    VSL_10 = ("VSL-1.0", "Vovida Software License v1.0")
    VIM = ("Vim", "Vim License")
    W3C = ("W3C", "W3C Software Notice and License (2002-12-31)")
    W3C_19980720 = ("W3C-19980720", "W3C Software Notice and License (1998-07-20)")
    W3C_20150513 = (
        "W3C-20150513",
        "W3C Software Notice and Document License (2015-05-13)",
    )
    WTFPL = ("WTFPL", "Do What The F*ck You Want To Public License")
    WATCOM_10 = ("Watcom-1.0", "Sybase Open Watcom Public License 1.0")
    WSUIPA = ("Wsuipa", "Wsuipa License")
    X11 = ("X11", "X11 License")
    XFREE86_11 = ("XFree86-1.1", "XFree86 License 1.1")
    XSKAT = ("XSkat", "XSkat License")
    XEROX = ("Xerox", "Xerox License")
    XNET = ("Xnet", "X.Net License")
    YPL_10 = ("YPL-1.0", "Yahoo! Public License v1.0")
    YPL_11 = ("YPL-1.1", "Yahoo! Public License v1.1")
    ZPL_11 = ("ZPL-1.1", "Zope Public License 1.1")
    ZPL_20 = ("ZPL-2.0", "Zope Public License 2.0")
    ZPL_21 = ("ZPL-2.1", "Zope Public License 2.1")
    ZED = ("Zed", "Zed License")
    ZEND_20 = ("Zend-2.0", "Zend License v2.0")
    ZIMBRA_13 = ("Zimbra-1.3", "Zimbra Public License v1.3")
    ZIMBRA_14 = ("Zimbra-1.4", "Zimbra Public License v1.4")
    ZLIB = ("Zlib", "zlib License")
    BLESSING = ("blessing", "SQLite Blessing")
    BZIP2_105 = ("bzip2-1.0.5", "bzip2 and libbzip2 License v1.0.5")
    BZIP2_106 = ("bzip2-1.0.6", "bzip2 and libbzip2 License v1.0.6")
    COPYLEFT_NEXT_030 = ("copyleft-next-0.3.0", "copyleft-next 0.3.0")
    COPYLEFT_NEXT_031 = ("copyleft-next-0.3.1", "copyleft-next 0.3.1")
    CURL = ("curl", "curl License")
    DIFFMARK = ("diffmark", "diffmark license")
    DVIPDFM = ("dvipdfm", "dvipdfm License")
    ECOS_20 = ("eCos-2.0", "eCos license version 2.0")
    EGENIX = ("eGenix", "eGenix.com Public License 1.1.0")
    ETALAB_20 = ("etalab-2.0", "Etalab Open License 2.0")
    GSOAP_13B = ("gSOAP-1.3b", "gSOAP Public License v1.3b")
    GNUPLOT = ("gnuplot", "gnuplot License")
    IMATIX = ("iMatix", "iMatix Standard Function Library Agreement")
    LIBPNG_20 = ("libpng-2.0", "PNG Reference Library version 2")
    LIBSELINUX_10 = ("libselinux-1.0", "libselinux public domain notice")
    LIBTIFF = ("libtiff", "libtiff License")
    MPICH2 = ("mpich2", "mpich2 License")
    PSFRAG = ("psfrag", "psfrag License")
    PSUTILS = ("psutils", "psutils License")
    WXWINDOWS = ("wxWindows", "wxWindows Library License")
    XINETD = ("xinetd", "xinetd License")
    XPP = ("xpp", "XPP License")
    ZLIB_ACKNOWLEDGEMENT = (
        "zlib-acknowledgement",
        "zlib/libpng License with Acknowledgement",
    )


class Domain(enum.Enum):
    """The domain to which the library belongs."""

    PYPI = "pypi"
    RUBYGEMS = "rubygems"
    NPM = "npm"


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True)
    library_id = Column(Integer, ForeignKey("libraries.id"))
    spdx = Column(Enum(Spdx))
    basis = Column(Enum(Basis))
    source_url = Column(String(256))

    library = relationship("Library", back_populates="licenses")

    def to_dict(self) -> Dict[str, str]:
        return {
            "spdx_id": self.spdx.value[0] if self.spdx is not None else None,
            "basis": self.basis.name if self.basis is not None else None,
            "source_url": self.source_url,
        }


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True)
    domain = Column(Enum(Domain))
    name = Column(String(32), index=True)
    version = Column(String(16))
    download_url = Column(String(256))
    homepage = Column(String(256))
    git_url = Column(String(256), nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    licenses = relationship("License", back_populates="library")

    __table_args__ = (
        UniqueConstraint("domain", "name", "version"),
        Index("index_domain_name", "domain", "name"),
        Index("index_name_version", "name", "version"),
    )

    def to_dict(self) -> Dict[str, str]:
        dic = {
            "domain": self.domain.value,
            "name": self.name,
            "version": self.version,
            "licenses": [lic.to_dict() for lic in self.licenses],
            "download_url": self.download_url,
            "homepage": self.homepage,
            "git_url": self.git_url,
        }
        if self.updated_at is not None:
            dic["updated_at"] = self.updated_at.isoformat()
        return dic


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
