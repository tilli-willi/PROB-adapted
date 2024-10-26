import json
from pycocotools import mask


def burst2coco(burst_annotation_file_path, coco_annotation_file_dest):
    # Load the burst annotation file
    with open(burst_annotation_file_path, "r") as file:
        burst_annotations = json.load(file)
    sequences = burst_annotations["sequences"]

    # Create a dictionary for the COCO style annotation
    with open(
        "/home/uig93971/src/PROB/datasets/annot_conversion/coco_annot_template.json",
        "r",
    ) as file:
        coco_annotations = json.load(file)

    img_id = 0
    obj_id = 0
    for seq in sequences:
        print(seq["dataset"] + "    " + seq["seq_name"])
        for img, segm in zip(seq["annotated_image_paths"], seq["segmentations"]):
            img_id = img_id + 1
            coco_img_entry = {
                "license": 0,
                "file_name": seq["dataset"] + "/" + seq["seq_name"] + "/" + img,
                "coco_url": "",
                "height": seq["height"],
                "width": seq["width"],
                "date_captured": "",
                "flickr_url": "",
                "id": img_id,
            }
            coco_annotations["images"].append(coco_img_entry)

            for track_id, instance in segm.items():
                obj_id = obj_id + 1
                rle = {
                    "size": [
                        seq["height"],
                        seq["width"],
                    ],  # provide the height and width of the image
                    "counts": instance[
                        "rle"
                    ],  # this is your RLE encoded mask as a string
                }
                coco_annot_entry = {
                    "segmentation": [],
                    "area": 0,
                    "iscrowd": 0,
                    "image_id": img_id,
                    "bbox": mask.toBbox(rle).tolist(),
                    "category_id": seq["track_category_ids"][track_id],
                    "id": obj_id,
                }
                coco_annotations["annotations"].append(coco_annot_entry)

    # Write the COCO-style annotations to the destination file
    with open(coco_annotation_file_dest, "w") as file:
        json.dump(coco_annotations, file, indent=4)


if __name__ == "__main__":
    burst_annotation_file_path = (
        "/home/uig93971/src/data/TAO/burst_annotations/val/all_classes.json"
    )
    coco_annotation_file_dest = (
        "/home/uig93971/src/data/TAO/burst_annotations/val/all_val_coco_style.json"
    )
    burst2coco(burst_annotation_file_path, coco_annotation_file_dest)
