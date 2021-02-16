from abdesign.core.anarciobject import AnarciObject

class IgObject:
    def __init__(self, seq, chain_type=None, species=None, iso_type=None, annotation=None, regions=None, humaness_score=None, hits=None):
        self._seq = seq
        self._chain_type = chain_type
        self._species = species
        self._iso_type = iso_type

        if annotation is None or isinstance(annotation,AnarciObject):
            self._annotation = annotation
        else:
            raise TypeError(f"Annotation is not of Type AnarciObject or None {type(annotation)}. Please check core.anarciObject.")

        if regions is None or isinstance(regions, AnarciObject):
            self._regions = regions
        else:
            raise TypeError(f"Regions are not of Type AnarciObject or None {type(regions)}. Please check core.anarciObject.")

        self._humaness_score = humaness_score
        self._hits = hits
        
    def __str__(self):
        return f"IgObject(\n\tseq={self.sequence},\n\tchain_type={self.chain_type},\n\tspecies={self.species},\n\tiso_type={self.iso_type},\n\tannotation={self.annotation},\n\tregions={self.regions},\n\thumaness_score={self.humaness_score},\n\thits={self.hits}\n)"

    @property 
    def sequence(self):
        return self._seq

    @property
    def chain_type(self):
        return self._chain_type

    @property
    def species(self):
        return self._species

    @property
    def iso_type(self):
        return self._iso_type

    @property
    def annotation(self):
        return self._annotation.dataframe

    @property
    def regions(self):
        return self._regions.dataframe

    @property
    def humaness_score(self):
        return self._humaness_score

    @property
    def hits(self):
        return self._hits

    # TODO: Make function work with new data format
    # def get_region(self,region='kabat'):
    #     """Function prints every region for different annotation systems, if the object was annotated with this system before. 
        
    #     Parameters
    #     ----------
    #     region : string, optional
    #         String representing an annotation system. , by default 'kabat'
        
    #     Raises
    #     ------
    #     TypeError
    #         Raises when regions input is not a string.
    #     KeyError
    #         Raises if IgObject was not annotated with the requested annotation system.
    #     """
    #     if not isinstance(region,str):
    #         raise TypeError("Please enter region in str format e.g. 'kabat'. Only 1 region allowed.")
    #     try:
    #         return self.regions[region]
    #     except KeyError:
    #         raise KeyError(f"Could not find '{key}' in IgObjects regions.")

    def get_position(self,annotation_type,position=None):
        if annotation_type:
            annotation_type = str(annotation_type)
            if position is not None:
                position = str(position)
                query = str(f"annotation_type == '{annotation_type}' and position == '{position}'")
            else:
                query = str(f"annotation_type == '{annotation_type}'")
            results = self.annotation.query(query)
            if results is not None:
                return results
            return "No position matching your criteria"
    
    # # TODO: Make function work with new data format
    # def get_best_hit(self):
    #     best_hit_key = list(self.hits)[0]
    #     return self.hits[best_hit_key]