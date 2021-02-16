import re # parsing anarci.output 
import pandas as pd
import subprocess # use for execute anarci
from tempfile import NamedTemporaryFile
import json # handling json for db
from abdesign.data.protein_iupac import valid_amino_acids
from collections.abc import Iterable
from abdesign.data.cdr_library import library
from abdesign.core.igobject import IgObject
from abdesign.core.anarciobject import AnarciObject

# maybe extract to IgObject
def _check_annotation_format(annotation):
    if annotation is None:
        return annotation
    else:
        if isinstance(annotation,Iterable):
            for elem in annotation:
                if not isinstance(annotation[elem],AnarciObject):
                    raise ValueError("Unknown format. Please check your annotation data or let the data generated automatically.")
            return annotation
        else:
            raise ValueError("Unknown format. Please check your annotation data or let the data generated automatically.")

def _all_params_present(ig_object):
    """Function to check whether al params of an IgObject are present
    
    Parameters
    ----------
    ig_object : IgObject
        Object to be checked
    
    Returns
    -------
    Bool
        Returns True if all params are present and not None
    
    Raises
    ------
    ValueError
        Raises if one param is missing
    """
    params = [ig_object.annotation,ig_object.regions,ig_object.sequence,ig_object.chain_type]
    if any(elem is None for elem in params):
        raise ValueError("No param can be 'None'.")
    return True

def _is_igobject(ig_object):
    if isinstance(ig_object,IgObject):
        return True
    raise TypeError("")

def create_annotation(sequence, anno_types=["kabat", "chothia", "imgt", "martin"]):
    if isinstance(anno_types,str):
        anno_types = [anno_types]
    seq = _init_seq(sequence)
    df_annotation = pd.DataFrame()
    df_regions = pd.DataFrame()

    for i, anno_type in enumerate(anno_types):
        chain_type, species, annotation = _annotate_sequence(seq,anno_type)
        extended_annotation = _process_anarci_data(anno_type,annotation,chain_type)
        region = _set_regions(anno_type,annotation)
        df_annotation = df_annotation.append(extended_annotation)
        df_regions = df_regions.append(region)

    annotations = AnarciObject(dataframe = df_annotation, indices=['annotation_type','position'])
    regions = AnarciObject(dataframe = df_regions, indices=['annotation_type','region'])

    ig_object = IgObject(seq=seq, chain_type=chain_type,species=species, annotation=annotations, regions=regions)

    return ig_object

def _init_seq(sequence):
    """Validation of sequence on initialization
    
    Parameters
    ----------
    sequence : string
        string representing the amino acid sequence
    
    Returns
    -------
    string
        sequence is returned if validation is successfull
    
    Raises
    ------
    TypeError
        Sequence have to be of type string

    ValueError
        All symbols have to be part of the official IUPAC Amino acid codes
    """
    if not isinstance(sequence,str):
        raise TypeError(f"Please enter a valid Input (e.g. EIVLTQSPGTLSLSPGERATLSCRASQSVSSSYL  ... ), Invalid: {sequence}")
    if sequence == "":
        raise ValueError("Sequence can not be empty")
    for i, l in enumerate(sequence):
        if not l.upper() in valid_amino_acids:
            raise ValueError(f"Invalid Sequence. Position: {i+1} | Character: '{l}'")
    return sequence.upper()

def _init_chain_type(chain_type):
    """Validation of chain type on initialization
    
    Parameters
    ----------
    `chain_type` : { "heavy", "h", "light", "kappa", "k", "lambda", "l", "alpha", "a", "beta", "b" }
        word / letter representing the chain_type .
        NOTE: "l" is representing the chain type "lambda", NOT "light".
    
    Returns
    -------
    String
        Returns a string representing the chain type if validation is successfull
    
    Raises
    ------
    ValueError
        If the `chain_type` is not part of valid chain types
    """
    if chain_type:
        valid_chain_types = ["heavy", "h","light", "l", "kappa", "lambda", "alpha", "beta", "a", "b", "k"]
        if not chain_type.lower() in valid_chain_types:
            raise ValueError(f"Please select a valid chain type! {valid_chain_types}")
        return chain_type.lower()
    else:
        return None

def _annotate_sequence(sequence,annotation_type="kabat"):
    """Function creates annotation data with anarci based on an given IgObject (which includes the sequence) 
    and a list of annotation systems. Currently there are just three annotation systems (["kabat","imgt","chothia"]) allowed.
    
    Parameters
    ----------
    ig_object : IgObject
        IgObject contains search sequence. This sequnce is used for annotation with anarci. The annotation data is a new attribute (self.annotation) of 
        format Dataframe.
    input_annotation_types : list
        List which includes the different annotation systems that should applied on IgObject as strings.
    
    Returns
    -------
    IgObject
        Returns new IgObject with attribute .annotation which contains a dictonary wit all applied 
        annotation systems where the key is represented by the annotation system. 
    
    Raises
    ------
    ValueError
        Raises if annotation type is unknown.
    ValueError
        Raises if Anarci could not annotate. In most cases the IgObject does not contain an Ig-Sequence.
    TypeError
        Raises if ig_object is not an instance of IgObject class.
    """
    valid_annotation_types = ["kabat","imgt","chothia","martin"]
    if annotation_type not in valid_annotation_types:
        raise ValueError(f"Unknown annotation type. Please check your given annotation types.")
    tmp_file_anarci = NamedTemporaryFile(prefix=annotation_type+"_",delete=False)
    tmp_file_hitfile = NamedTemporaryFile(prefix=annotation_type+"_hitfile_",delete=False)
    process = subprocess.run(['ANARCI','-i',sequence,"-o",tmp_file_anarci.name,"-ht",tmp_file_hitfile.name,"-s",annotation_type], check=True, stdout=subprocess.PIPE, universal_newlines=True)      
    output = process.stdout
    errors = process.stderr
    if errors:
        print("Errors",errors)
    with open(tmp_file_anarci.name) as file:
        lines = file.readlines()
        if lines == ['# Input sequence\n', '//\n']:
            raise ValueError("Couldn't identify Ig-Object. Please check your sequence.")
        datalist = []
        imgt_position = 0
        for i, line in enumerate(lines):
            if i == len(lines)-1:
                continue
            parsed_line = re.split("#|\||\n|    |   |  ", line)
            parsed_line = list(filter(None, parsed_line))
            if i == 4:
                keys = parsed_line
            if i == 5:
                values = parsed_line
            if i > 6:
                chain = parsed_line[0][0]
                amino_acid = parsed_line[1][-1]
                position = parsed_line[0][2:]
                if len(parsed_line[1]) > 2:
                    extension = parsed_line[1][0]
                else:
                    extension = None
                datalist.append([annotation_type,chain,str(position),extension,amino_acid])
        meta = dict(zip(keys,values))
        datalist = pd.DataFrame(datalist, columns=["annotation_type","chain","position","extension","amino_acid"]) # Removes last line -> //
        annotation = AnarciObject.dataframe = datalist
        chain_type = meta['chain_type']
        species = meta['species']
    return chain_type, species, annotation

def _read_hits(file):
    with open(file) as f:
        lines = f.readlines()
        hits_obj = {}
        entries = []
        for i, line in enumerate(lines):
            parsed_line = re.split("#|\||\n|    |   |  | |description", line)
            parsed_line = list(filter(None, parsed_line))
            if i == 4:
                head = parsed_line
            if i >= 5 and i < len(lines)-1:
                entries.append(parsed_line)
        for e in entries:
            hits_obj[e[0]] = dict(zip(head,e))
    return hits_obj

def _process_anarci_data(annotation_type,annotation,chain_type):
    """Function that adds cdr column based on annotation system and position
    
    Parameters
    ----------
    annotation_type : str
        Name of annotation type 

    annotation : pd.Dataframe

    chain_type : str
    
    Returns
    -------
    pd.Dataframe
        New annotation object
    
    Raises
    ------
    ValueError
        Raises if chain type is invalid
    """
    if chain_type == None:
        raise ValueError("Cannot read chain type.")
    if not chain_type in ["heavy", "h", "H"]:
        chain_type = "light"
    else:
        chain_type = "heavy"
    annotation["cdr"] = "FR"
    for p in range(1,4):
        annotation.loc[
            (annotation["position"].astype(int) >= int(library[annotation_type][chain_type][f"start_{p}"])) & 
            (annotation["position"].astype(int) <= int(library[annotation_type][chain_type][f"end_{p}"]["num"])) 
            , "cdr"] = f"CDR{p}"
        annotation.loc[
            (annotation["cdr"].str.contains("CDR")) &
            (_check_positioning(annotation["extension"]) > _check_library(library[annotation_type][chain_type][f"end_{p}"]["ext"]))
            , "cdr" ] = ""
    return annotation

def _check_positioning(series):
    """Returns a Series of unicode numbers of an given Series object
    
    Parameters
    ----------
    series : Series
        Dataframe Series containing an alphabetical character
    
    Returns
    -------
    Series or integer
        returns Series with unicode numbers representing the alphabetical symbol or '1' if TypeError occurs.
    """
    try:
        return series.apply(lambda x: ord(x))
    except TypeError:
        return 1

def _check_library(string):
    """Returns a unicode number representing an alphabetical symbol
    
    Parameters
    ----------
    string : string
        String contains alphabetical symbol which should be transformed to unicode number
    
    Returns
    -------
    integer
        returns unicode number if transformation is successfull or '1' if TypeError occurs.
    """
    try:
        return (ord(string))
    except TypeError:
        return 1

def _set_regions(annotation_type, annotation):
    """Function to identify regions of annotated IgObjects and represent the results in table format.
    
    Parameters
    ----------
    annotation_type : str
        Name of annotation type 
    annotation: pd.Dataframe
        Dataframe with information about each position
    
    Returns
    -------
    pd.Dataframe
        Dataframe which provides a summary about each region of the sequence
    """
    cdr_summary = pd.DataFrame(columns=["annotation_type","region","sequence_fragment","residue","length"])
    region = ""
    counter = 0 #from 1 to 3
    deletion = 0
    cur_seq = ""
    seq_len = 0
    last_reload = 1
    for index, row in annotation.iterrows():
        current = row["cdr"]
        if index == 0:
            region = current
        if row['amino_acid'] not in valid_amino_acids:
            deletion +=1
            continue
        if not region == current:
            seq_len += len(cur_seq)
            if region == "FR":
                counter +=1
                df = pd.DataFrame({ "annotation_type": [f"{annotation_type}"],
                                    "region": [f"FR{counter}"],
                                    "sequence_fragment": [cur_seq],
                                    "residue": [f"{last_reload}-{seq_len}"],
                                    "length": [f"{len(cur_seq)}"]
                })
            else:
                df = pd.DataFrame({ "annotation_type": [f"{annotation_type}"],
                                    "region": [f"CDR{counter}"],
                                    "sequence_fragment": [cur_seq],
                                    "residue": [f"{last_reload}-{seq_len}"],
                                    "length": [f"{len(cur_seq)}"]
                })
            region = current
            start = index
            cdr_summary = cdr_summary.append(df)
            cur_seq = ""
            last_reload = seq_len+1
        cur_seq += row['amino_acid']
        if index == len(annotation)-1:
            counter +=1
            df_extra = pd.DataFrame({   "annotation_type": [f"{annotation_type}"],
                                        "region": [f"FR{counter}"],
                                        "sequence_fragment": [f"{cur_seq}"],
                                        "residue": [f"{last_reload}-{last_reload+len(cur_seq)-1}"],
                                        "length": [f"{len(cur_seq)}"]
            })
            cdr_summary = cdr_summary.append(df_extra)
    cdr_summary.reset_index(drop=True, inplace=True)
    return cdr_summary

def extract_cdr_and_fr(ig_object):
    """Extract cdr and framework region from annotated IgObject.
    
    Parameters
    ----------
    ig_object : IgObject
        Annotated IgObject.
    
    Returns
    -------
    IgObject
        New IgObject containig framework and cdrs as attributes for every annotation system.
    
    Raises
    ------
    ValueError
        No param can be 'None'.
    """
    params = [ig_object.annotation,ig_object.regions]
    if any(elem is None for elem in params):
        raise ValueError("No param can be 'None'.")
    extracted_cdr = {}
    extracted_fr = {}
    for key in ig_object.regions:
        dataframe = ig_object.regions[key]
        cdr = dataframe.iloc[[1,3,5],]
        fr = dataframe.iloc[[0,2,4,6],]
        extracted_cdr[key] = cdr
        extracted_fr[key] = fr
    ig_object.cdrs = extracted_cdr
    ig_object.fr = extracted_fr
    return ig_object

def _concat_sequence(df):
    """Function that concatenates sequence fragment which are located in one Dataframe column. 
    Gets Dataframe and column name.
    
    Parameters
    ----------
    df : pd.Dataframe
        Dataframe contains regions information and sequence fragment column.
    column_name : str, optional
        Column name of column with sequence fragments, by default "Sequence Fragment"
    
    Returns
    -------
    string
        Concatenated sequence fragments.
    
    Raises
    ------
    TypeError
        df input is no instance of pandas.Dataframe
    """
    if isinstance(df,AnarciObject):
        return "".join(df['Sequence Fragment'].tolist())
    else:
        raise TypeError("pandas Dataframe expected. Wrong format.")


def export_to_json(ig_object,to_file=True, filename="igobject.json"):
    """Function to export a whole IgObject to a file or a new object in json-format.
    
    Parameters
    ----------
    ig_object : IgObject
        IgObject which should be exported.
    to_file : bool, optional
        Decides whether json-object should returned or write, by default True
    filename : string, optional
        Filename, by default "igobject.json"
    
    Returns
    -------
    json
        If to_file=False, json object is returned
    """
    
    if _all_params_present(ig_object):

        annotation_json = _translate_to_valid_json(ig_object.annotation)
        regions_json = _translate_to_valid_json(ig_object.regions)

        export_object = {
                        "meta":{
                            "seq":ig_object.sequence,
                            "chain_type": ig_object.chain_type,
                            "species": ig_object.species,
                            "humaness": ig_object.humaness_score
                            },
                        "data": {
                            "regions": regions_json,
                            "annotation": annotation_json
                            }
                        }

        if to_file:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_object, f, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            return json.dumps(export_object, ensure_ascii=False, indent=4, sort_keys=True)

def save_hitfile(ig_object,filename):
    """Function to export hitlist created by anarci
    
    Parameters
    ----------
    ig_object : IgObject
        Annotated IgObject
    filename : string, optional
        Filename, by default "hitfile.json"
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(ig_object.hits,f,ensure_ascii=False, indent=3, sort_keys=True)

def _translate_to_valid_json(obj):
    """Function to create json object out of dictonary with pandas Dataframes
    
    Parameters
    ----------
    obj : dict
        Dictonary containing pandas Dataframes (e.g. .annotation, .regions)
    
    Returns
    -------
    json
        Json object for further processing
    """
    ig_object_table = obj.copy()
    exp_obj = {}
    keys = set()
    for elem in ig_object_table.index:
        keys.add(elem[0])
    for key in keys:
        subset = ig_object_table.xs(key)
        new_set = subset.reset_index()
        exp_obj[key] = new_set.to_json()
    return exp_obj
