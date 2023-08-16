import json
import argparse
import os 
import sys

def read_json(file_path):
    if os.path.exists(file_path) == False:
        sys.exit("Original BDD100K file not found at: {}".format(file_path))
    with open(file_path) as f:
        d = json.load(f)
    return d


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--det_train_path", 
            default="BDD100K/det_train.json", 
            help="Original BDD100K train labels file path"
    )
    parser.add_argument("--det_val_path", 
            default="BDD100K/det_val.json", 
            help="Original BDD100K val labels file path"
    )
    parser.add_argument("--outpath", 
            default="BDD100K", 
            help="Output path. Default is: ./BDD100k"
    )
    args = parser.parse_args()
    return args


def merge(custom_labels, det_split):
    image_with_additional_labels = {}
    for i, d in enumerate(custom_labels):
        image_with_additional_labels[d["name"]] = i

    dataset = []
    for d in det_split:
        img_name = d["name"]
        if img_name in image_with_additional_labels.keys():
            original_labels = d['labels']
            for obj in original_labels:
                if obj["category"] == "traffic light":
                    idx = obj["id"]
                    additional_labels = custom_labels[image_with_additional_labels[d["name"]]]["labels"]
                    for tl in additional_labels:
                        if tl["id"] == idx:
                            obj["attributes"]["trafficLightRelevant"] = tl["trafficLightRelevant"]
                            continue
                else:
                    obj["attributes"]["trafficLightRelevant"] = False
            dataset.append(d)
    return dataset


def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    args = parse_args()
    
    # load traffic light relevance labels
    custom_labels_train = read_json("BDD100K/det_train_only_traffic_light_relevance.json")
    custom_labels_val = read_json("BDD100K/det_val_only_traffic_light_relevance.json")
    
    # load original BDD100K labels
    det_train = read_json(args.det_train_path)
    det_val= read_json(args.det_val_path)

    # Merge
    print("\nMerging train...")
    det_train_merged = merge(custom_labels_train, det_train)
    print("\nMerging val...")
    det_val_merged = merge(custom_labels_val, det_val)

    print("\nStoring files...")
    write_json(os.path.join(args.outpath, "det_train_merged.json"), det_train_merged)
    write_json(os.path.join(args.outpath, "det_val_merged.json"), det_val_merged)

    print("\nDONE")


                    


    