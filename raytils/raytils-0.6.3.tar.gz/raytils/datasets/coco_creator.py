import json
import pathlib
import random
import shutil
import uuid
import warnings
from io import BytesIO, StringIO
from itertools import groupby
from typing import Optional, Dict

import cv2
import imagesize
import numpy as np
import requests
from PIL import Image
from rays_pycocotools import coco
from rays_pycocotools import mask as pycoco_mask
from tqdm import tqdm

import asyncio
from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor

from raytils.datasets.coco_fields import CocoCategories, CocoInfo, CocoLicence, CocoDetectionAnnotation, CocoModes, \
    CocoList, CocoImage, combine_coco_objects
from raytils.perception import get_image_size


class Annotation:
    def __init__(self, class_name, bbox=None, mask=None, classifications=None, kwargs=None):
        if classifications is None:
            classifications = []
        if kwargs is None:
            kwargs = {}
        if bbox is None and mask is None:
            raise ValueError("No annotations provided either bbox or mask must be valid")
        if not isinstance(classifications, list):
            raise TypeError("Classifications parameter must be a list!")
        if not isinstance(class_name, str):
            raise TypeError("Class name parameter must be a string!")
        self.class_name = class_name
        self.classifications = classifications
        self.kwargs = kwargs
        self._bbox = bbox
        self._mask = mask
        self.__bbox_area = 0
        self.__mask_area = 0
        _, _, self._bbox, self._mask = self.valid()  # Force numpy arrays or large memory hogs to lowest representation


    def valid(self):
        bbox, poly = self.bbox, self.poly
        valid_bbox, valid_poly = sum([x == 0 for x in bbox]) != len(bbox), poly and bool(poly[0])
        return valid_bbox, valid_poly, bbox, poly

    @property
    def area(self):
        _, _ = self.poly, self.bbox  # Getters may set area
        if self.__mask_area:
            return self.__mask_area
        if self.__bbox_area:
            return self.__bbox_area
        return 0

    @property
    def poly(self):
        # TODO: Find general purpose way of doing this (mask->segm, RLE->segm, RLEencoded->segm)
        # TODO: Currently only supports RLEencoded->segm
        if self._mask is None:  # Return None if no poly
            return self._mask

        if isinstance(self._mask, list) and any(isinstance(el, list) for el in self._mask):
            return self._mask  # Must already be a list of poly lists
        elif isinstance(self._mask, (np.ndarray, dict)):  # If mask or RLE then get contours
            if isinstance(self._mask, dict):  # RLE
                if isinstance(self._mask['counts'], (bytes, list)):
                    # Decode RLE to mask
                    if isinstance(self._mask['counts'], list):
                        rle = coco.maskUtils.frPyObjects(self._mask, self._mask["size"][0], self._mask["size"][1])
                    else:
                        rle = self._mask
                    mask = coco.maskUtils.decode(rle)

                    if self._bbox is None:
                        self._bbox = list(coco.maskUtils.toBbox(rle))
                else:
                    raise ValueError("Mask is not a valid RLE dict")
            else:  # Must already be mask?
                mask = self._mask

            # Decode the binary mask
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            segmentation = [[]]
            if contours:
                segmentation = [c.flatten().tolist() for c in contours if c.size > 4]

            if self._bbox is None:
                xfl = [i for j in segmentation for idx, i in enumerate(j) if idx % 2 == 0]
                yfl = [i for j in segmentation for idx, i in enumerate(j) if idx % 2 != 0]
                x, y = min(xfl), min(yfl)
                w, h = max(xfl) - x, max(yfl) - y
                self._bbox = [x, y, w, h]

            self.__mask_area = np.count_nonzero(mask)
            self._mask = segmentation  # Change mask to poly to save memory
            return self._mask
        elif isinstance(self._mask, list) and not isinstance(self._mask[0], list) and len(self._mask) % 2 == 0:
            self._mask = [self._mask]  # Mask must already be a poly
            return self._mask

        raise ValueError("Invalid value for mask ({})".format(type(self._mask)))

    @property
    def bbox(self):
        if self._bbox:
            self.__bbox_area = self._bbox[-2] * self._bbox[-1]
            return self._bbox

        _ = self.poly  # Poly may set the bounding box

        if self._bbox is None:
            raise ValueError("Cannot automatically infer bounding box")

        return self._bbox


class COCOCreator:
    """ Class for creating annotation files in COCO format through a simple interface

    Attributes:
        mode: Coco annotation file type e.g "detection" or "keypoints"
        data_splits: Dictionary describing the export format (useful for splitting into training/testing splits)
        random_splits: Shuffle the imported data between data_splits if true
    """

    # TODO: Finish implementation
    #  - Add support for multiple different file imports (csv, json, images etc)
    #  - Add support for different modes (Keypoint, Panoptic, Instance Segm etc)
    def __init__(self, mode: str, data_splits: Optional[Dict[str, float]] = None, random_splits=True):
        if not CocoModes.is_valid(mode):
            raise ValueError(f"Mode '{mode}' isn't a valid COCO format\n\tMust be one of: {CocoModes.modes}")
        self.__mode = mode
        if self.__mode != CocoModes.DETECTION:
            raise NotImplementedError(f"Export of {self.__mode} coco files is not currently implemented")
        if data_splits is None:
            data_splits = {"coco": 1.0}
        if 0 > sum(data_splits.values()) > 1.0:
            raise ValueError(f"Cannot split dataset into '{data_splits}' data splits are not between 0 and 1!")
        self.data_splits = data_splits
        self.random_splits = random_splits
        self.__image_path_ann_lut = {}
        self.__extra_fields_lut = {}
        self.classes = CocoCategories()
        self.info = CocoInfo(contributor="Raymond Kirk", url="https://github.com/RaymondKirk")
        self.license = CocoLicence(licence_id=0, name="Contact Author", url="https://github.com/RaymondKirk")
        self.licenses = CocoList([self.license])

    def map_classes(self, map_dict):
        """Replace classes in keys of map_dict with value"""
        for key, annotations in self.__image_path_ann_lut.items():
            for ann in annotations:
                if ann.class_name in map_dict:
                    ann.class_name = map_dict[ann.class_name]
        for old, new in map_dict.items():
            if old in self.classes:
                self.classes.remove(old)
            else:
                warnings.warn(f"Class '{old}' does not exist. Adding new class '{new}' anyway.")
            self.classes.add(new)

    def remove_classes(self, classes):
        """Replace classes in keys of map_dict with value"""
        for key in self.__image_path_ann_lut.keys():
            self.__image_path_ann_lut[key] = [x for x in self.__image_path_ann_lut[key] if x.class_name not in classes]

        for old in classes:
            self.classes.remove(old)

    def add_classes(self, classes):
        if not isinstance(classes, list):
            classes = [classes]
        for cls in classes:
            self.classes.add(cls)

    def add_detection_annotation(self, image_path, class_name, bbox=None, mask=None, classifications=None, kwargs=None):
        if self.__mode != CocoModes.DETECTION:
            raise ValueError(f"Cannot call add_detection_annotation when creating a {self.__mode} coco file")
        image_path = str(image_path)  # Ensure it's a string not Path object
        if image_path not in self.__image_path_ann_lut:
            self.__image_path_ann_lut[image_path] = []
        annotation = Annotation(class_name, bbox, mask, classifications, kwargs)
        self.__image_path_ann_lut[image_path].append(annotation)
        self.classes.add(class_name)

    def add_detection_image(self, image_path):
        if self.__mode != CocoModes.DETECTION:
            raise ValueError(f"Cannot call add_detection_annotation when creating a {self.__mode} coco file")
        image_path = str(image_path)  # Ensure it's a string not Path object
        if image_path not in self.__image_path_ann_lut:
            self.__image_path_ann_lut[image_path] = []

    def add_images_with_masks(self, image_list, mask_list, classes_list):
        """Adds detections from an image and corresponding binary mask"""
        for image_path, mask_path, mask_class in zip(image_list, mask_list, classes_list):
            image_path, mask_path = pathlib.Path(image_path), pathlib.Path(mask_path)
            assert image_path.name == mask_path.name
            mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
            if mask.shape[:2] != img.shape[:2]:
                mask = cv2.resize(mask, (img.shape[:2])[::-1])
            self.add_detection_annotation(image_path, mask_class, None, mask)

    def add_images_with_greyscale_mask(self, image_list, mask_list, classes_list):
        """Adds detections from an image and corresponding greyscale mask (multiple annotations to an image)"""
        for image_path, mask_path, mask_class in tqdm(total=zip(image_list, mask_list, classes_list),
                                                      postfix="Adding images from segmentation masks"):
            image_path, mask_path = pathlib.Path(image_path), pathlib.Path(mask_path)
            assert image_path.name == mask_path.name
            masks = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
            if masks.shape[:2] != img.shape[:2]:
                masks = cv2.resize(masks, (img.shape[:2])[::-1])
            unique_values = np.unique(masks)
            unique_values = unique_values[unique_values != 0].tolist()
            for mask_idx in unique_values:
                mask = np.zeros_like(masks)
                mask[np.where(masks == mask_idx)] = 255.0
                self.add_detection_annotation(image_path, mask_class, None, mask)

    def add_coco_json(self, json_path, image_root=None):
        """Adds detections from a coco file"""
        if isinstance(json_path, str):
            json_path = pathlib.Path(json_path)
        if image_root is None:
            image_root = json_path.parent
        with json_path.open("rb") as fh:
            coco_data = json.load(fh)

        image_id_to_filename = {c["id"]: c["file_name"] for c in coco_data["images"]}
        category_id_to_class_name = {c["id"]: c["name"] for c in coco_data["categories"]}
        for annotation in coco_data["annotations"]:
            bbox = annotation.get("bbox")
            segm = annotation.get("segmentation")
            class_name = category_id_to_class_name[annotation["category_id"]]
            file_name = image_root / image_id_to_filename[annotation["image_id"]]
            self.add_detection_annotation(file_name, class_name, bbox, segm)

    def add_darwin_v7(self, json_path):
        """Adds detections from a V7 darwin json file"""
        if isinstance(json_path, str):
            json_path = pathlib.Path(json_path)
        with json_path.open("rb") as fh:
            darwin = json.load(fh)

        file_id_to_name = {str(idx): d for idx, d in enumerate(darwin["image"]["frame_urls"])}
        for path in file_id_to_name.values():  # add all images in-case of no annotations for image
            self.add_detection_image(path)

        annotations = {}  # frame_id: [annotations]
        for ann in darwin["annotations"]:
            class_name = ann["name"]
            interpolated = ann["interpolated"]
            # validate all instance_ids are consistent
            ids = set([ii["instance_id"]["value"] for ii in ann["frames"].values() if "instance_id" in ii])
            if not ids:
                continue
            if len(ids) > 1:
                raise ValueError("Instance IDS not unique")
            instance_id = ids.pop()
            for frame_id, frame_annotation in ann["frames"].items():
                bbox = [frame_annotation["bounding_box"].get(a) for a in ["x", "y", "w", "h"]]
                if frame_id not in annotations:
                    annotations[frame_id] = []
                self.add_detection_annotation(image_path=file_id_to_name[frame_id], bbox=bbox, class_name=class_name,
                                              kwargs=dict(instance_id=instance_id, interpolated=interpolated,))

    def add_label_box_export_async(self, json_path, num_workers=64):
        """Converts a LabelBox JSON (https://app.labelbox.com/) instance segmentation file to COCO"""
        async def get_label_box_async(json_file_path):
            def fetch(requests_session, item):
                rgb_file = item["Labeled Data"]
                objects = item["Label"]["objects"]
                max_attempts = 20
                status = "Done"

                for o in objects:
                    mask_url = o["instanceURI"]
                    attempts = 0
                    while attempts <= max_attempts:
                        r = requests_session.get(mask_url)
                        if r.status_code != 200:
                            print(
                                f"\nError code {r.status_code}={r.reason} for {mask_url} (attempt={attempts}/{max_attempts})")
                            if attempts == max_attempts:
                                print(f"Skipping {rgb_file}, too many failed attempts")
                                status = "Error"
                                break
                            attempts += 1
                            continue
                        mask = np.asfortranarray(Image.open(BytesIO(r.content)), dtype=np.uint8)[..., 0]
                        mask[mask > 0] = 1.0
                        rle = pycoco_mask.encode(mask)
                        classifications = [a["value"] for i in o.get("classifications", []) for a in i["answers"]]
                        self.add_detection_annotation(rgb_file, o["value"], mask=rle, classifications=classifications)
                        break

                elapsed = default_timer() - async_loop_start_time
                time_completed_at = "{:5.2f}s".format(elapsed)
                progress_bar.set_postfix_str("{} with {} at {}".format(status, rgb_file, time_completed_at))
                progress_bar.update(1)

            if isinstance(json_file_path, str):
                json_file_path = pathlib.Path(json_file_path).resolve()

            with json_file_path.open("r") as fh:
                json_data = json.load(fh)

            # Initialize the event loop
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                with requests.Session() as session:
                    progress_bar = tqdm(total=len(json_data))
                    async_loop_start_time = default_timer()

                    tasks = [
                        loop.run_in_executor(
                            executor,
                            fetch,
                            *(session, item)
                        )
                        for item in json_data
                    ]

                    # Initializes the tasks to run and awaits their results
                    for response in await asyncio.gather(*tasks):
                        pass

                    progress_bar.close()

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_label_box_async(json_path))
        loop.run_until_complete(future)

    def add_label_me_folder(self, folder_path):
        """Converts a LabelMe (https://github.com/wkentaro/labelme) instance segmentation folder to COCO"""
        if isinstance(folder_path, str):
            folder_path = pathlib.Path(folder_path).resolve()

        json_files = list(folder_path.glob("*.json"))

        if not len(json_files):
            raise IOError("No '.json' files in the label me folder '{}'!".format(folder_path))

        for file in tqdm(total=json_files, postfix=f"Detections from LabelMe Folder {folder_path}"):
            with file.open("rb") as fh:
                label_data = json.load(fh)
            image_path = (folder_path / label_data["imagePath"]).resolve()
            if not image_path.is_file():
                raise IOError("File '{}' does not exists!".format(image_path))

            for shape in label_data['shapes']:
                if "points" not in shape:
                    raise NotImplementedError("Only LabelMe files labelled as polygons are supported")
                points_list = [item for xy in shape['points'] for item in xy]
                x1, x2 = min([xy[0] for xy in shape['points']]), max([xy[0] for xy in shape['points']])
                y1, y2 = min([xy[1] for xy in shape['points']]), max([xy[1] for xy in shape['points']])
                w, h = x2 - x1, y2 - y1
                label_no_digits = ''.join(i for i in shape["label"] if not i.isdigit())
                # TODO: Calculate mask area instead of bbox
                self.add_detection_annotation(image_path, label_no_digits, bbox=[x1, y1, w, h], mask=points_list)

    def add_extra_info(self, image_path, **kwargs):
        """Adds extra info to a CocoImage field. Useful for things such as depth.
            If adding extra file paths you must also copy the files before or after exporting.
        """
        if image_path not in self.__image_path_ann_lut:
            raise ValueError(f"Annotations for '{image_path}' have not been added yet. Please add them first.")

        if image_path not in self.__extra_fields_lut:
            self.__extra_fields_lut[image_path] = {}
        for field_name, field_info in kwargs.items():
            self.__extra_fields_lut[image_path][field_name] = field_info

    def export(self, dataset_root: pathlib.Path, *args, **kwargs):
        if self.__mode == CocoModes.DETECTION:
            return self.export_detection(dataset_root, *args, **kwargs)
        raise NotImplementedError(f"Mode  '{self.__mode}' is not currently supported.")

    def export_detection(self, output_dir: pathlib.Path, symlink_to_image: bool = False, exists_ok: bool = False):
        if isinstance(output_dir, str):
            output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        class_name_to_idx = self.classes.classes_to_idx

        image_id = 0

        image_path_lut = self.__image_path_ann_lut
        packaged_image_path_lut = {}
        progress_bar_post_fix = ("Creating symlink to" if symlink_to_image else "Copying") + " image data '{}'"
        progress_bar = tqdm(total=len(image_path_lut), postfix=progress_bar_post_fix.format(""))

        images_not_local = False
        tmp_dir = f"/tmp/coco_creator/{uuid.uuid4()}"

        # Write image data to new packaged dataset
        for image_file, image_annotation in image_path_lut.items():
            original_file = image_file
            # Download the file if it doesn't exist locally
            if "http://" in image_file or "https://" in image_file:
                images_not_local = True
                tmp_file = pathlib.Path(f"{tmp_dir}/{pathlib.Path(image_file).name}")
                tmp_file.parent.mkdir(exist_ok=True)
                with tmp_file.open("wb") as handle:
                    response = requests.get(image_file, stream=True)
                    if not response.ok:
                        raise IOError("Could not download image_file")
                    progress_bar.set_postfix_str(f"Downloading {image_file}")
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                image_file = type(original_file)(tmp_file)

            if not pathlib.Path(image_file).exists():
                print(f"Skipping '{image_file}' as it does not exist on the filesystem")
                continue
            progress_bar.set_postfix_str(progress_bar_post_fix.format(image_file))

            width, height = get_image_size(image_file)

            # Copy the files to new COCO dataset
            new_image_file = f"data/{image_id}_{pathlib.Path(image_file).name}"
            new_image_file_location = output_dir / new_image_file
            new_image_file_location.parent.mkdir(exist_ok=True, parents=True)
            if symlink_to_image:  # Symlink if parameter is set else copy the file
                if images_not_local:
                    raise IOError("Cannot symlink to images if they're not stored locally")
                try:
                    pathlib.Path(new_image_file_location).symlink_to(pathlib.Path(image_file),
                                                                     target_is_directory=False)
                except FileExistsError:
                    if not exists_ok:  # sometimes if combining datasets the file will exist in multiple coco files
                        raise
            else:
                shutil.copy(str(image_file), str(new_image_file_location))

            packaged_image_path_lut[new_image_file] = (CocoImage(
                image_id=image_id,
                width=width,
                height=height,
                file_name=new_image_file,
                image_license=self.license.id,
                flickr_url="",
                coco_url=original_file,
                date_captured="",
                **self.__extra_fields_lut.get(image_file, {})
            ), image_path_lut[original_file])

            image_id += 1
            progress_bar.update()
        progress_bar.close()
        del image_path_lut

        # Split files randomly into n-sized data split sections
        data_split_keys = list(self.data_splits.keys())
        data_split_values = [self.data_splits[k] for k in data_split_keys]
        split_sizes = [int(round(len(packaged_image_path_lut) * v)) for v in data_split_values]
        idx_splits = [0] + [sum(split_sizes[:l]) for l in range(1, len(split_sizes) + 1)]
        file_path_keys = list(packaged_image_path_lut.keys())
        if self.random_splits:
            random.shuffle(file_path_keys)
        # Always export an _combined.json file unless this is what the user is exporting/only one file exported
        all_data_splits_file = '_'.join(self.data_splits.keys()) + '_combined'
        if len(self.data_splits.keys()) > 1 and all_data_splits_file not in self.data_splits:
            split_keys = {all_data_splits_file: file_path_keys}
        else:
            split_keys = dict()
        split_keys.update({data_split_keys[i]: file_path_keys[idx_splits[i]:idx_splits[i + 1]]
                           for i in range(0, len(idx_splits) - 1)})

        # Write COCO image (training/testing/all etc splits)
        for split_name, file_paths in split_keys.items():
            annotation_id = 0
            annotations = CocoList()
            export_file_name = output_dir / "{}.json".format(split_name)
            export_file_name.parent.mkdir(parents=True, exist_ok=True)

            progress_bar_post_fix = f" Exporting {export_file_name}: " + "'{}'"
            progress_bar = tqdm(total=len(packaged_image_path_lut), postfix=progress_bar_post_fix.format(""))
            coco_images = CocoList()
            split_packaged_lut = {k: packaged_image_path_lut[k] for k in file_paths}

            for image_file, (coco_image, image_annotation) in split_packaged_lut.items():
                coco_images.append(coco_image)
                for idx, ann in enumerate(image_annotation):
                    progress_bar.set_postfix_str(
                        progress_bar_post_fix.format(f"{idx + 1}/{len(image_annotation)} {image_file}")
                    )
                    valid_bbox, valid_poly, bbox, poly = ann.valid()
                    if not valid_bbox:  # mini
                        continue
                    annotations.append(CocoDetectionAnnotation(
                        annotation_id=annotation_id,
                        image_id=coco_image.id,
                        category_id=class_name_to_idx[ann.class_name],
                        segmentation=poly,
                        area=ann.area,
                        bbox=bbox,
                        iscrowd=0,
                        classifications=ann.classifications,
                        **ann.kwargs
                    ))
                    annotation_id += 1
                progress_bar.update()
            progress_bar.close()
            coco_file = combine_coco_objects([self.info, coco_images, annotations, self.classes, self.licenses])

            with export_file_name.open('w') as fh:
                json.dump(coco_file, fh, indent=4, sort_keys=True)
