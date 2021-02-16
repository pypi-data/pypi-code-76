from abdesign.util.annotation import _all_params_present
from abdesign.core.igobject import IgObject
from abdesign.core.anarciobject import AnarciObject
from abdesign.util.annotation import create_annotation
import pandas as pd

def replace_cdr(igquery: IgObject,igtarget: IgObject, annotation_types=['kabat','chothia','imgt']):
    """Function which gets two IgObjects (Query and Target) and generates a new hybrid IgObject.
    

    Parameters
    ----------
    igquery : IgObject
        Object representing the Query-Sequence which is annotated and contains CDRs. CDRs from this object 
        were extracted and integrated in FR regions from Target region.
    igtarget : IgObject
        Object representing the Target-Sequence which is annotated and contains FR.
    annotation_type : string
        String representing an annotation type. 
    
    Returns
    -------
    IgObject
        Returns new annotated IgObject.
    """
    if _all_params_present(igquery) and _all_params_present(igtarget):
        igquery_regions = igquery.regions
        igtarget_regions = igtarget.regions
        same_anno_type = False
        for item in list(igquery_regions.index):
            if item in list(igtarget_regions.index):
                same_anno_type = item[0]
                break
        if not same_anno_type:
            raise ValueError("Non matching anno types found")
        dfcolumns = ["annotation_type","region",'sequence_fragment', 'residue', 'length']
        df_hybrid = AnarciObject(dataframe=pd.DataFrame(columns=dfcolumns),indices=['annotation_type','region'])
        df_hybrid = df_hybrid.dataframe
        df_query = igquery_regions.xs(same_anno_type)
        df_target = igtarget_regions.xs(same_anno_type)
        df_hybrid = df_hybrid.append(df_target.loc[df_target.index.str.contains('FR1')])
        df_hybrid = df_hybrid.append(df_query.loc[df_query.index.str.contains('CDR1')])
        df_hybrid = df_hybrid.append(df_target.loc[df_target.index.str.contains('FR2')])
        df_hybrid = df_hybrid.append(df_query.loc[df_query.index.str.contains('CDR2')])
        df_hybrid = df_hybrid.append(df_target.loc[df_target.index.str.contains('FR3')])
        df_hybrid = df_hybrid.append(df_query.loc[df_query.index.str.contains('CDR3')])
        df_hybrid = df_hybrid.append(df_target.loc[df_target.index.str.contains('FR4')])
        df_hybrid.reset_index()
        concat_seq = ""
        for i, line in df_hybrid.iterrows():
            concat_seq += line.sequence_fragment

    hybrid_ig_obj = create_annotation(concat_seq, anno_types=annotation_types)
    return hybrid_ig_obj
