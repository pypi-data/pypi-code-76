        # Small optimization for HDF5 files: If we have the raw CSV, we can convert to
        # feather. We can't do this for Columnar files because we don't know the
        # column types
        if datafile.feather_path is None:
            if datafile_format == DataFileFormat.HDF5:
                feather_path = self._get_path_and_make_directories(
                    datafile.full_taiga_id, ".feather"
                )
                try:
                    _write_csv_to_feather(
                        datafile.raw_path, feather_path, datafile_format, None, None
                    )
                    c.execute(
                        """
                        UPDATE datafiles
                        SET 
                            feather_path = ?
                        WHERE
                            full_taiga_id = ?
                        """,
                        (feather_path, datafile.full_taiga_id),
                    )
                except Exception:
                    self.remove_from_cache(queried_taiga_id)
            else:
                return None
