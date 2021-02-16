import json
from abdesign.data.cdr_library import library
from abdesign.core.igobject import IgObject
from abdesign.util.annotation import *
from abdesign.core.anarciobject import AnarciObject

if __name__ == "__main__":
    antibody = create_annotation("ELVMTQSPSSLSASVGDRVNIACRASQGISSALAWYQQKPGKAPRLLIYDAYYYSNLESGVPSRFSGSGSGTDFTLTISSLQPEDFAIYYCQQFNSYPLTFGGGTKVEIKRTV",anno_types=["kabat","imgt"])
    print(antibody)
    #print(antibody.get_position('kabat',40))
    #print(antibody.get_position('imgt', 120))
    # a = MultiIndex()
    # print(a)
    #s#ave_hitfile(antibody,"hitfile.json")
    #export_to_json(antibody)