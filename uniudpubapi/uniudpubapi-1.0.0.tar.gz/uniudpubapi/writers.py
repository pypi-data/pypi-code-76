from bibtexparser.bwriter import BibTexWriter
from abc import ABC, abstractmethod
from bibtexparser.bibdatabase import BibDatabase
from .dep_pubs import DepartmentPublications
import os


class PublicationWriter(ABC):
    """Abstract class for writing publications to files

    Methods
    -------
    export(path)
        exports all the publications
    """

    def __init__(self, dep_pubs: DepartmentPublications) -> None:
        """constructor

        Parameters
        ----------
        dep_pubs
            publication of the department
        """

        self._dep_pubs = dep_pubs
    
    def _create_dir(self, path:str) -> None:
        try:
            if not os.path.exists(path):
                os.mkdir(path, 0o755)
        except OSError:
            print("Creation of the directory failed {}", path)


    @abstractmethod
    def export(self, path: str = "./pubs/"):
        pass


class BibtexPublicationWriter(PublicationWriter):
    """ Use this class for writing publications in bibtex format
    """



    def export(self, path: str = "./pubs/") -> None:
        """overrides superclass abstract method

        For each publication will be created a new folder with the title
        of that publication as the name of the folder.
        The bibtex file is named "cite.bib"  and written inside the folder previously
        created.

        Parameters
        ----------
        path : optional
            path where files should be saved, by default "./pubs/"

        Raises
        ------
        KeyError
            if the type of publication and the handle are not specified
        """
        self._create_dir(path)
        for pub in self._dep_pubs:
            meta = pub.get_bibtex_representation()
            if not meta:
                print("This pub has no meta")
            else:
                if meta["type"] and meta["handle"]:
                    handle = meta.pop("handle")
                    pub_type = meta.pop("type")
                    db = BibDatabase()
                    db.entries = [meta.copy()]
                    db.entries[0].update({"ID": handle, "ENTRYTYPE": pub_type})
                    writer = BibTexWriter()
                    tot = []
                    for key in meta:
                        tot.append(key)
                    # To keep the order of the elements inside the bibtex file
                    writer.display_order = tot
                    try:
                        # Bibtex representation title has curly braces
                        # meta["title"] = meta["title"][1:len(meta["title"]) - 1]
                        my_dir = meta["title"].replace("/", "_").replace(" ", "-") \
                            .replace("\"", "")
                        full_path = path + my_dir
                        if not os.path.exists(full_path):
                            os.mkdir(full_path, 0o755)
                            with open(full_path + "/" + "cite.bib", "w") \
                                    as bibfile:
                                bibfile.write(writer.write(db))
                        else:
                            with open(full_path + "/" + "cite.bib", "w") \
                                    as bibfile:
                                bibfile.write(writer.write(db))
                    except OSError:
                        print("Creation of the directory failed {}", my_dir)
                else:
                    raise KeyError("the type of publication and metdata"
                                   + "are required")

    def export_to_bibtex_one_file(self, path: str = "all.bib"):
        """stores publications in bibtex format in one file

        Parameters
        ----------
        path : optional
            path where the resulting file should be stored, by default "all.bib"

        Raises
        ------
        KeyError
            if the type of publication and the handle are not specified
        """
        self._create_dir(path)
        for pub in self._dep_pubs:
            meta = pub.get_bibtex_representation()
            if not meta:
                print("This pub has no meta")
            else:
                if meta["type"] and meta["handle"]:
                    handle = meta.pop("handle")
                    pub_type = meta.pop("type")
                    db = BibDatabase()
                    db.entries = [meta.copy()]
                    db.entries[0].update({"ID": handle, "ENTRYTYPE": pub_type})
                    writer = BibTexWriter()
                    tot = []
                    for key in meta:
                        tot.append(key)
                    writer.display_order = tot
                    with open(path, "a") as bibfile:
                        bibfile.write(writer.write(db))
                else:
                    raise KeyError("the type of publication and metdata"
                                   + "are required")


class MarkdownPublicationWriter(PublicationWriter):
    """Use this class for writing publications in markdown format
    """

    def export(self, path: str = "./pubs/"):
        """overrides superclass abstract method

        For each publication will be created a new folder with the title
        of that publication as the name of the folder.
        The markdown file is named "index.md"  and written inside the folder
        previously created.

        Parameters
        ----------
        path : optional
            path where files should be saved, by default "./pubs/"
        """
        for item in self._dep_pubs:
            md_string = "--- \n"
            pub_meta = item.get_site_meta()
            for key, value in pub_meta.items():
                md_string += key + ": " + value
                md_string += "\n"
            md_string += "---"

            try:
                my_dir = pub_meta["title"].replace("/", "_").replace("\"", "") \
                    .replace(" ", "-")
                full_path = path + my_dir
                if not os.path.exists(full_path):
                    os.mkdir(full_path, 0o755)
                    with open(full_path + "/" + "index.md", "w") \
                            as md_file:
                        md_file.write(md_string)
                else:
                    with open(full_path + "/" + "index.md", "w") \
                            as md_file:
                        md_file.write(md_string)
            except OSError:
                print("Creation of the directory failed {}", full_path)
