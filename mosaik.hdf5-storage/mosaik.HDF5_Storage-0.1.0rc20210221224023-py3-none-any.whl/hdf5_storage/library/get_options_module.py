import hdf5storage


def get_options():
    options: hdf5storage.Options = hdf5storage.Options(
        store_python_metadata=True,
        matlab_compatible=False,  # TODO
        action_for_matlab_incompatible='error',
        delete_unused_variables=False,
        structured_numpy_ndarray_as_struct=False,
        make_atleast_2d=False,
        convert_numpy_bytes_to_utf16=False,
        convert_numpy_str_to_utf16=False,
        convert_bools_to_uint8=False,
        reverse_dimension_order=False,
        store_shape_for_empty=False,
        complex_names=('r', 'i'),
        group_for_references='/#refs#',
        oned_as='row',
        compress=True,
        compress_size_threshold=16384,
        compression_algorithm='gzip',
        gzip_compression_level=7,
        shuffle_filter=True,
        compressed_fletcher32_filter=True,
        uncompressed_fletcher32_filter=False,
        marshaller_collection=None,
    )

    return options
