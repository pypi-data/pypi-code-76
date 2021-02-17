from pathlib import Path

import open3d as o3d  # type: ignore

from pycarus.datasets.shapenet_part import ShapeNetPartSegmentation


def main() -> None:
    path_ds = "../ShapeNetPart/"
    dataset = ShapeNetPartSegmentation(path_root=Path(path_ds), split="train", download=True)
    print(len(dataset))

    for index, sample in enumerate(dataset):  # type: ignore
        name = dataset.samples[index]
        category = dataset.ids_to_categories[dataset.classes[sample[1]]]

        print(f"Name: {name[0]} - Category: {category}.")
        o3d.visualization.draw_geometries([ShapeNetPartSegmentation.show_item(sample)])


if __name__ == "__main__":
    main()
