# coding=utf-8

"""Abstraction for communicating with an XNAT server"""


import abc
import os

import pydicom
import urllib3

from copyxnat.xnat.xml_cleaner import XmlCleaner, XnatType


class XnatServerParams:
    """Encapsulates parameters used to access an XNAT server"""

    def __init__(self, host, user, pwd, insecure=False, read_only=False):
        if '://' not in host:
            host = 'https://' + host
        self.host = host
        self.user = user
        self.pwd = pwd
        self.insecure = insecure
        self.read_only = read_only


class XnatBase(abc.ABC):
    """Base class for an item in the XNAT data hierarchy"""

    def __init__(self, parent_cache, interface, label, read_only, xml_cleaner,
                 app_settings, reporter, parent):
        self.parent = parent
        self.interface = interface
        if not label:
            reporter.warning("An empty label was found for a {} type".
                             format(self._name))  # pylint: disable=no-member
        self.label = label or "unknown"
        self.cache = parent_cache.sub_cache(self._cache_subdir_name, label)  # pylint: disable=no-member
        self.read_only = read_only
        self.full_name = self.cache.full_name
        self.xml_cleaner = xml_cleaner
        self.reporter = reporter
        self.app_settings = app_settings
        self.label_map = {self._xml_id: label}  # pylint: disable=no-member
        if parent:
            for item_tag, item_label in parent.label_map.items():
                self.label_map[item_tag] = item_label

    def fetch_interface(self):
        """Get the XNAT backend interface for this object"""
        return self.interface.fetch_interface()

    def user_visible_info(self):
        """String representation of this object that can be shown to user"""
        level = self.cache.cache_level
        return '  '*level + '-({}) {}'.format(self._name, self.label)  # pylint: disable=no-member

    def get_children(self, ignore_filter) -> list:
        """Return XNAT child objects of this XNAT object"""

        # Iterate through XnatItem classes that are child types of this class,
        # but filter out ones the Command has indicated to exclude
        consider_types = [child for child in self._child_types if child not in  # pylint: disable=no-member
                          ignore_filter]

        for child_class in consider_types:

            # Call the defined PyXnatItem method to get the interfaces, and
            # wrap each in an XnatItem
            for item in getattr(self.interface, child_class.interface_method)():
                yield child_class.get_existing(interface=item, parent=self)

    @abc.abstractmethod
    def metadata_missing(self):
        """Return True if this item or any parent requires metadata which could
        be found from the child Files"""

    @abc.abstractmethod
    def provide_metadata(self, metadata):
        """Supply missing metadata to parent items"""


class XnatItem(XnatBase):
    """Base class for data-level item in the XNAT data hierarchy. Used for all
    non-root items (ie all items other than XnatServer) """

    def __init__(self, interface, label, parent):

        super().__init__(parent_cache=parent.cache,
                         interface=interface,
                         label=label,
                         read_only=parent.read_only,
                         reporter=parent.reporter,
                         app_settings=parent.app_settings,
                         xml_cleaner=parent.xml_cleaner,
                         parent=parent)

    @classmethod
    def get_existing(cls, interface, parent):
        """
        Return XnatItem for the provided interface which must represent an
        item that already exists on the server. Error if it does not exist.
        :return: a new XnatItem corresponding to the inteerface
        """
        label = interface.get_label()
        if not interface.exists():
            raise ValueError('{} {} should already exist under {} but was '
                             'not found'.
                             format(cls._name, label, parent.full_name))  # pylint: disable=no-member
        return cls(interface=interface, label=label, parent=parent)

    def copy(self, destination_parent, app_settings, dst_label=None):
        """
        Make a copy of this item on a different server, if it doesn't already
        exist, and return an XnatItem interface to the duplicate item.

        :destination_parent: parent XnatItem under which to make the duplicate
        :app_settings: global settings
        :dst_label: label for destination object, or None to use source label
        :return: a new XnatItem corresponding to the duplicate item
        """
        duplicate = self.duplicate(destination_parent, app_settings, dst_label)
        return duplicate

    def duplicate(self, destination_parent, app_settings, dst_label=None):
        """
        Make a copy of this item on a different server, if it doesn't already
        exist, and return an XnatItem interface to the duplicate item.

        :destination_parent: parent XnatItem under which to make the duplicate
        :dst_label: label for destination object, or None to use source label
        :return: a new XnatItem corresponding to the duplicate item
        """

        label = dst_label or self.label
        copied_item = self.get_or_create_child(parent=destination_parent,
                                               label=label)

        if copied_item.exists_on_server():
            if app_settings.overwrite_existing:
                self.reporter.warning("Updating existing {} {}".
                                      format(self._name, label))  # pylint: disable=no-member
                write_dst = True
            else:
                self.reporter.warning("Skipping {} {} (already exists on "
                                      "destination)".format(self._name, label))  # pylint: disable=no-member
                write_dst = False
        else:
            write_dst = True

        if write_dst:
            self.create(dst_item=copied_item)

        return copied_item

    def progress_update(self, reporter):
        """Update the user about current progress"""

    def get_or_create_child(self, parent, label):
        """
        Create an XNAT item under the specified parent if it does not already
        exist, and return an XnatItem wrapper that can be used to access this
        item.

        :parent: The XnatItem under which the child will be created if it does
            not already exist
        :label: The identifier used to find or create the child item
        :create_params: Additional parameters needed to create child item
        :local_file: path to a local file containing the resource or XML data
            that should be used to create this object on the server if
            it doesn't already exist
        :dry_run: if True then no change will be made on the destination server
        :return: new XnatItem wrapping the item fetched or created

        """

        cls = self.__class__
        interface = self.interface.create(parent_pyxnatitem=parent.interface,
                                          label=label)

        return cls(interface=interface,
                   label=label,
                   parent=parent)

    def create_on_server(self, create_params, local_file):
        """Create this item on the XNAT server"""
        if self.app_settings.dry_run:
            print('DRY RUN: did not create {} {} with file {}'.
                  format(self._name, self.label, local_file))  # pylint: disable=protected-access, no-member
        else:
            self.interface.create_on_server(
                local_file=local_file,
                create_params=create_params,
                overwrite=self.app_settings.overwrite_existing,
                reporter=self.reporter
            )

    def exists_on_server(self):
        """Return True if item already exists on the XNAT server"""
        return self.interface.exists()

    @abc.abstractmethod
    def export(self, app_settings) -> str:
        """Save this item to the cache"""

    @abc.abstractmethod
    def create(self, dst_item):
        """
        Create a local file copy of this item, with any required
        cleaning so that it is ready for upload to the destination server

        :destination_parent: parent XnatItem under which to make the duplicate
        :label: The identifier used to find or create the child item
        :return: tuple of local file path, additional creation parameters
        """

    def ohif_generate_session(self):
        """Trigger regeneration of OHIF session data"""

    def request(self, uri, method, warn_on_fail=True):
        """Execute a REST call on the server"""
        return self.parent.request(uri, method, warn_on_fail)

    def ohif_present(self):
        """Return True if the OHIF viewer plugin is installed"""
        return self.parent.ohif_present()

    def rebuild_catalog(self):
        """Send a catalog refresh request"""

    def post_create(self):
        """Post-processing after item creation"""

    def metadata_missing(self):
        """Return True if this item or any parent requires metadata which could
        be found from the child Files"""
        return self._metadata_missing() or self.parent.metadata_missing()

    def provide_metadata(self, metadata):
        self._provide_metadata(metadata)
        self.parent.provide_metadata(metadata)

    def _metadata_missing(self):  # pylint: disable=no-self-use
        return False

    def _provide_metadata(self, metadata):  # pylint: disable=no-self-use
        pass


class XnatParentItem(XnatItem):
    """
    Base class for item in the XNAT data hierarchy which can contain
    resources and child items
    """

    def get_xml_string(self):
        """Get an XML string representation of this item"""
        return self.interface.get_xml_string()

    def get_xml(self):
        """Get an XML representation of this item"""
        return XmlCleaner.xml_from_string(self.get_xml_string())

    def create(self, dst_item):

        # Note that cleaning will modify the xml_root object passed in
        cleaned_xml_root = self.clean(
            xml_root=self.get_xml(),
            fix_scan_types=self.app_settings.fix_scan_types,
            destination_parent=dst_item.parent,
            label=dst_item.label
        )
        local_file = self.cache.write_xml(
            cleaned_xml_root, self._xml_filename)  # pylint: disable=no-member

        dst_item.create_on_server(create_params=None, local_file=local_file)

        if local_file:
            os.remove(local_file)

    def clean(self, xml_root, fix_scan_types, destination_parent, label):  # pylint: disable=unused-argument
        """
        Modify XML values for items copied between XNAT projects, to allow
        for changes in unique identifiers.

        :xml_root: parent XML node for the xml contents to be modified
        :fix_scan_types: if True then ambiguous scan types will be corrected
        :destination_parent: parent XnatItem under which to make the duplicate
        :label: label for destination object
        :return: the modified xml_root
        """
        return self.xml_cleaner.clean(
            xml_root=xml_root,
            xnat_type=self._xml_id,  # pylint: disable=no-member
            fix_scan_types=fix_scan_types)

    def copy(self, destination_parent, app_settings, dst_label=None):
        duplicate = super().copy(destination_parent, app_settings, dst_label)

        if duplicate:
            # Update the maps that are used to modify attributes in child items
            src_xml_root = self.get_xml()
            final_xml_root = duplicate.get_xml()  # pylint: disable=no-member
            self.xml_cleaner.add_tag_remaps(src_xml_root=src_xml_root,
                                            dst_xml_root=final_xml_root,
                                            xnat_type=self._xml_id,  # pylint: disable=no-member
                                            )

        return duplicate

    def export(self, app_settings):
        src_xml_root = self.get_xml()
        return self.cache.write_xml(src_xml_root, self._xml_filename)  # pylint: disable=no-member


class XnatFileContainerItem(XnatItem):
    """Base wrapper for resource items"""

    def create(self, dst_item):
        if self.app_settings.download_zips:
            folder_path = self.cache.make_output_path()
            local_file = self.interface.download_zip_file(folder_path)
        else:
            local_file = None

        dst_item.create_on_server(create_params=None, local_file=local_file)

        if local_file:
            os.remove(local_file)

    def export(self, app_settings):
        folder_path = self.cache.make_output_path()
        if not app_settings.download_zips:
            return folder_path

        return self.interface.download_zip_file(folder_path)


class XnatFile(XnatItem):
    """Base wrapper for file items"""

    _name = 'File'
    _xml_id = XnatType.file
    _cache_subdir_name = 'files'
    interface_method = 'files'
    _child_types = []

    def create(self, dst_item):
        folder_path = self.cache.make_output_path()
        attributes = self.interface.file_attributes()
        local_file = self.interface.download_file(folder_path)
        dst_item.create_on_server(create_params=attributes,
                                  local_file=local_file)
        if local_file:
            self._add_missing_metadata(local_file=local_file)
            os.remove(local_file)

    def copy(self, destination_parent, app_settings, dst_label=None):
        if app_settings.download_zips:
            return None
        return super().copy(destination_parent=destination_parent,
                            app_settings=app_settings,
                            dst_label=dst_label)

    def export(self, app_settings):
        if app_settings.download_zips:
            return None

        folder_path = self.cache.make_output_path()
        return self.interface.download_file(folder_path)

    def user_visible_info(self):
        base_string = super().user_visible_info()
        attrs = self.interface.file_attributes()
        attr_string = ' (content:{}, format:{}, tags:{})'.format(
            attrs.get('file_content'),
            attrs.get('file_format'),
            attrs.get('file_tags'))

        return base_string + attr_string

    def ohif_generate_session(self):
        # Use files to supply missing metadata
        self._add_missing_metadata()

    def _add_missing_metadata(self, local_file=None):
        tmp_local_file = None
        if not local_file:
            folder_path = self.cache.make_output_path()
            tmp_local_file = self.interface.download_file(folder_path)
            local_file = tmp_local_file

        if self.metadata_missing():
            metadata = self._parse_metadata(local_file)

            if metadata:
                self.provide_metadata(metadata)

        if tmp_local_file:
            os.remove(tmp_local_file)

    def _parse_metadata(self, local_file):  # pylint: disable=no-self-use
        metadata = {}
        try:
            if pydicom.misc.is_dicom(local_file):
                tags = pydicom.dcmread(
                    local_file,
                    stop_before_pixels=True,
                    specific_tags=[
                        pydicom.datadict.tag_for_keyword('SeriesInstanceUID')]
                )
                metadata['series_instance_uid'] = \
                    tags['SeriesInstanceUID'].value

        except Exception as exc:  # pylint: disable=broad-except
            self.reporter.warning('Error when attempting to parse file {}: '
                                  'Error: {}'.format(local_file, exc))
        return metadata


class XnatResource(XnatFileContainerItem):
    """Wrapper for access to an XNAT resource"""

    _name = 'Resource'
    _xml_id = XnatType.resource
    _cache_subdir_name = 'resources'
    interface_method = 'resources'
    _child_types = [XnatFile]


class XnatInResource(XnatFileContainerItem):
    """Wrapper for access to an XNAT resource"""

    _name = 'In_Resource'
    _xml_id = XnatType.in_resource
    _cache_subdir_name = 'in_resources'
    interface_method = 'in_resources'
    _child_types = [XnatFile]


class XnatOutResource(XnatFileContainerItem):
    """Wrapper for access to an XNAT resource"""

    _name = 'Out_Resource'
    _xml_id = XnatType.out_resource
    _cache_subdir_name = 'out_resources'
    interface_method = 'out_resources'
    _child_types = [XnatFile]


class XnatReconstruction(XnatParentItem):
    """Wrapper for access to an XNAT assessor"""

    _name = 'Reconstruction'
    _cache_subdir_name = 'reconstructions'
    _xml_filename = 'metadata_reconstruction.xml'
    _xml_id = XnatType.reconstruction
    interface_method = 'reconstructions'
    _child_types = [XnatInResource, XnatOutResource]


class XnatAssessor(XnatParentItem):
    """Wrapper for access to an XNAT assessor"""

    _name = 'Assessor'
    _cache_subdir_name = 'assessors'
    _xml_filename = 'metadata_assessor.xml'
    _xml_id = XnatType.assessor
    interface_method = 'assessors'
    _child_types = [XnatResource, XnatInResource, XnatOutResource]

    def rebuild_catalog(self):
        uri = 'data/services/refresh/catalog?' \
              'options=populateStats%2Cappend%2Cdelete%2Cchecksum&' \
              'resource=/archive/projects/{}/subjects/{}/experiments/{}'.format(
                self.label_map[XnatProject._xml_id],  # pylint: disable=protected-access
                self.label_map[XnatSubject._xml_id],  # pylint: disable=protected-access
                self.interface.get_id())
        self.request(uri, 'POST', warn_on_fail=True)


class XnatScan(XnatParentItem):
    """Wrapper for access to an XNAT scan"""

    _name = 'Scan'
    _xml_filename = 'metadata_scan.xml'
    _cache_subdir_name = 'scans'
    _xml_id = XnatType.scan
    interface_method = 'scans'
    _child_types = [XnatResource]

    def __init__(self, interface, label, parent):
        self._metadata = {'UID': None}
        super().__init__(interface, label, parent)

    def _metadata_missing(self):
        if not self._metadata['UID']:
            self._metadata['UID'] = self.interface.fetch_interface().\
                attrs.get('UID')
        return not all(self._metadata.values())

    def _provide_metadata(self, metadata):
        if (not self._metadata['UID']) and ('series_instance_uid' in metadata):
            uid = metadata['series_instance_uid']
            current_uid = self.interface.fetch_interface().attrs.get('UID')
            if current_uid:
                if not current_uid == uid:
                    self.reporter.warning(
                        'The scan UID is {} but a DICOM file has a series '
                        'instance UID of {}. Will not modify the scan UID'.
                        format(current_uid, uid))
            else:
                self.reporter.warning('Setting Scan UID to {}'.format(uid))
                self.interface.fetch_interface().attrs.set('UID', uid)


class XnatExperiment(XnatParentItem):
    """Wrapper for access to an XNAT experiment"""

    _name = 'Experiment'
    _xml_filename = 'metadata_session.xml'
    _cache_subdir_name = 'experiments'
    _xml_id = XnatType.experiment
    interface_method = 'experiments'
    _child_types = [XnatScan, XnatAssessor, XnatReconstruction, XnatResource]

    def post_create(self):
        self.ohif_generate_session()

    def ohif_generate_session(self):
        if self.ohif_present():
            uri = 'xapi/viewer/projects/{}/experiments/{}'.format(
                self.label_map[XnatProject._xml_id],  # pylint: disable=protected-access
                self.interface.get_id())
            self.request(uri, 'POST', warn_on_fail=True)

    def rebuild_catalog(self):
        uri = 'data/services/refresh/catalog?' \
              'options=populateStats%2Cappend%2Cdelete%2Cchecksum&' \
              'resource=/archive/projects/{}/subjects/{}/experiments/{}'.format(
                self.label_map[XnatProject._xml_id],  # pylint: disable=protected-access
                self.label_map[XnatSubject._xml_id],  # pylint: disable=protected-access
                self.interface.get_id())
        self.request(uri, 'POST', warn_on_fail=True)

    def progress_update(self, reporter):
        reporter.next_progress()


class XnatSubject(XnatParentItem):
    """Wrapper for access to an XNAT subject"""

    _name = 'Subject'
    _xml_filename = 'metadata_subject.xml'
    _cache_subdir_name = 'subjects'
    _xml_id = XnatType.subject
    interface_method = 'subjects'
    _child_types = [XnatExperiment, XnatResource]


class XnatProject(XnatParentItem):
    """Wrapper for access to an XNAT project"""

    _name = 'Project'
    _xml_filename = 'metadata_project.xml'
    _cache_subdir_name = 'projects'
    _xml_id = XnatType.project
    interface_method = 'projects'
    _child_types = [XnatSubject, XnatResource]

    def clean(self, xml_root, fix_scan_types, destination_parent,
              label):
        disallowed = destination_parent.get_disallowed_project_ids(label=label)
        cleaned_xml_root = self.xml_cleaner.make_project_names_unique(
            xml_root=xml_root,
            disallowed_ids=disallowed["secondary_ids"],
            disallowed_names=disallowed["names"]
        )

        return self.xml_cleaner.clean(
            xml_root=cleaned_xml_root,
            xnat_type=self._xml_id,  # pylint: disable=no-member
            fix_scan_types=fix_scan_types)


class XnatServer(XnatBase):
    """Access an XNAT server"""

    _name = 'Server'
    _cache_subdir_name = 'servers'
    _child_types = [XnatProject]
    _xml_id = XnatType.server

    def __init__(self,
                 factory,
                 params,
                 app_settings,
                 base_cache,
                 reporter
                 ):

        if params.insecure:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        interface = factory.create(params=params)

        self.ohif = None

        label = params.host.replace('https://', '').replace('http://', '')
        self._projects = None
        super().__init__(parent_cache=base_cache,
                         interface=interface,
                         label=label,
                         read_only=params.read_only,
                         app_settings=app_settings,
                         xml_cleaner=XmlCleaner(reporter=reporter),
                         reporter=reporter,
                         parent=None)

    def datatypes(self):
        """Return all the session datatypes in use on this server"""
        return self.interface.datatypes()

    def project_list(self):
        """Return array of project ids"""
        return self.interface.project_list()

    def project(self, label):
        """Return XnatProject for this project id"""
        return XnatProject.get_existing(
            interface=self.interface.project(label),
            parent=self)

    def logout(self):
        """Disconnect from this server"""
        self.interface.logout()

    def num_experiments(self, project):
        """Return number of experiments in this project"""
        return self.interface.num_experiments(project)

    def request(self, uri, method, warn_on_fail=True):
        """Execute a REST call on the server"""
        return self.interface.request(uri=uri,
                                      method=method,
                                      reporter=self.reporter,
                                      warn_on_fail=warn_on_fail)

    def ohif_present(self):
        """Return True if the OHIF viewer plugin is installed"""

        if self.ohif is None:
            self.ohif = self.request(
                uri='xapi/plugins/ohifViewerPlugin',
                method='GET',
                warn_on_fail=False)
        return self.ohif

    def get_disallowed_project_ids(self, label):
        """
        Return arrays of project names and secondary IDs that cannot be used
        for the destination project because they are already in use by other
        projects on this server. If the project already exists then the name
        and ID it is currently using are allowed (ie they will not be included
        in the disallowed lists).

        :param label: the label of the project which
        :return:
        """
        project_list = {project['ID']: project for project in
            self.fetch_interface()._get_json('/REST/projects')}  # pylint: disable=protected-access

        disallowed_secondary_ids = []
        disallowed_names = []
        for pr_id, project in project_list.items():
            if not pr_id == label:
                disallowed_names.append(project["name"])
                disallowed_secondary_ids.append(project["secondary_ID"])
        return {"names": disallowed_names,
                "secondary_ids": disallowed_secondary_ids}

    def metadata_missing(self):  # pylint: disable=no-self-use
        return False

    def provide_metadata(self, metadata):  # pylint: disable=no-self-use
        pass
