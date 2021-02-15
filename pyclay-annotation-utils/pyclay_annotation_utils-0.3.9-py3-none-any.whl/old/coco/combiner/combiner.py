from logger import logger
from common_utils.time_utils import get_present_year, get_present_time_Ymd
from common_utils.user_utils import get_username

from ..annotation import COCO_AnnotationFileParser
from ..structs import COCO_Info, COCO_License_Handler, COCO_Image_Handler, \
    COCO_Annotation_Handler, COCO_Category_Handler
from ..writer import COCO_Writer
from ...util.utils.coco import COCO_Mapper_Handler, COCO_Field_Buffer

def print_id_update(added_new: bool, old_id: int, new_id: int):
    header = 'ADDED' if added_new else 'LINKED'
    logger.info(f"{header}: {old_id} -> {new_id}")

class COCO_Annotations_Combiner:
    def __init__(self, img_dir_list: list, ann_path_list: list):
        # Constructor Parameters
        self.img_dir_list = img_dir_list
        self.ann_path_list = ann_path_list

        # Working Parameters
        self.buffer = COCO_Field_Buffer.from_scratch(
            description="COCO annotation generated by combining several coco annotations.",
            url='https://github.com/cm107/KeypointPose',
            version='1.0'
        )
        self.id_mapper = COCO_Mapper_Handler()

    def add_licenses(self, ann_key: str, coco_license_handler: COCO_License_Handler, verbose: bool=False):
        for coco_license in coco_license_handler.license_list:
            added_new, old_id, new_id = self.buffer.process_license(coco_license=coco_license, id_mapper=self.id_mapper, unique_key=ann_key)
            if verbose: print_id_update(added_new=added_new, old_id=old_id, new_id=new_id)

    def add_images(self, ann_key: str, coco_image_handler: COCO_Image_Handler, img_dir: str, update_img_paths: bool=True, verbose: bool=False):
        for coco_image in coco_image_handler.image_list:
            added_new, old_id, new_id = self.buffer.process_image(
                coco_image=coco_image, id_mapper=self.id_mapper, unique_key=ann_key, img_dir=img_dir, update_img_path=update_img_paths
            )
            if verbose: print_id_update(added_new=added_new, old_id=old_id, new_id=new_id)

    def add_annotations(self, ann_key: str, coco_annotation_handler: COCO_Annotation_Handler, verbose: bool=False):
        for coco_annotation in coco_annotation_handler.annotation_list:
            added_new, old_id, new_id = self.buffer.process_annotation(
                coco_annotation=coco_annotation, id_mapper=self.id_mapper, unique_key=ann_key
            )
            if verbose: print_id_update(added_new=added_new, old_id=old_id, new_id=new_id)

    def add_categories(self, ann_key: str, coco_category_handler: COCO_Category_Handler, verbose: bool=False):
        for coco_category in coco_category_handler.category_list:
            added_new, old_id, new_id = self.buffer.process_category(
                coco_category=coco_category, id_mapper=self.id_mapper, unique_key=ann_key
            )
            if verbose: print_id_update(added_new=added_new, old_id=old_id, new_id=new_id)

    def load_combined(self, update_img_paths: bool=True, verbose: bool=False, detailed_verbose: bool=False):
        for i, [img_dir, ann_path] in enumerate(zip(self.img_dir_list, self.ann_path_list)):
            if verbose: logger.info(f"{i}: Parsing {img_dir}, {ann_path}")
            parser = COCO_AnnotationFileParser(annotation_path=ann_path)
            parser.load(verbose=verbose)
            if verbose: logger.good("Annotations Loaded")
            self.add_licenses(ann_key=ann_path, coco_license_handler=parser.licenses, verbose=detailed_verbose)
            if verbose: logger.good(f"Licenses Updated")
            self.add_images(ann_key=ann_path, coco_image_handler=parser.images, img_dir=img_dir, update_img_paths=update_img_paths, verbose=detailed_verbose)
            if verbose: logger.good(f"Images Updated")
            self.add_categories(ann_key=ann_path, coco_category_handler=parser.categories, verbose=detailed_verbose)
            if verbose: logger.good(f"Categories Updated")
            self.add_annotations(ann_key=ann_path, coco_annotation_handler=parser.annotations, verbose=detailed_verbose)
            if verbose: logger.good(f"Annotations Updated")
        if verbose: logger.good(f"Finished Loaded Combined Annotations")

    def write_combined(self, output_path: str, verbose: bool=False):
        writer = COCO_Writer.from_buffer(buffer=self.buffer, output_path=output_path)
        json_dict = writer.build_json_dict(verbose=verbose)
        writer.write_json_dict(json_dict=json_dict, verbose=verbose)