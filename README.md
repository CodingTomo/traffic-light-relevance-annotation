# Introduction
This repository contains all the necessary information for constructing the dataset used to train the models and replicate the findings of the paper titled *Cross-model temporal cooperation via saliency maps for efficient recognition and classification of relevant traffic lights*.

# Dataset
The dataset used for training the models presented in the paper is a combination of two datasets: the DriveU Traffic Light Dataset (DTLD) and BDD100K. The decision to merge these datasets was driven by the goal of enhancing dataset diversity. While DTLD is a large dataset, it consists of European on-road images captured during daylight hours. On the other hand, BDD100K consists of images captured in a range of weather conditions and across North America.

The **relevance** attribute associated to each traffic light, which was utilized to assign labels to each image, was already included in the DTLD annotations but was absent in BDD100K. Therefore, we manually labeled the relevance attribute for the MOT (Multi-Object Tracking) subset of BDD100K. For a more comprehensive understanding of the relevance attribute and the proposed task, please refer to our paper.

The subsequent paragraph provides detailed instructions for constructing the dataset and reproducing the results outlined in the paper.


## DTLD
<p>
	<img src="/src/DTLD.jpg" alt="DTLD">
	<em>Image taken from DTLD dataset.</em>
</p>

As mentioned, DTLD already have the information about the relevance for the traffic lights. Since DTLD does not have a pre-defined validation split, we selected 296 out of the 1478 video sequences from the training split and used them for validation and we kept the original split for testing. The splits can be found in the DTLD folder.
    
    └── DTLD              
        ├── train.csv     # training split
        ├── val.csv       # validation split
        └── test.csv      # test split

Each CSV file contains three columns that uniquely identify a video segment. 

| city   	| route   	| intersection        	|
|--------	|---------	|---------------------	|
| Berlin 	| Berlin1 	| 2015-04-17_10-50-41 	|
| Berlin 	| Berlin1 	| 2015-04-17_10-51-12 	|
| ...    	| ...     	| ...                 	|

More information about the dataset could be found [HERE](https://www.uni-ulm.de/in/iui-drive-u/projekte/driveu-traffic-light-dataset/). 

## BDD100K
<p>
	<img src="/src/BDD.png" alt="BDD100k">
	<em>Image taken from BDD100K dataset.</em>
</p>

In the BDD100K dataset, the attribute of **relevance** associated to each traffic light respect to the ego-vehicle, which is present in the DTLD dataset, is not originally included in the annotations. To address this, we manually labeled the relevance attribute for each traffic light in every image of the MOT subset of BDD100K. These annotations can be found in the BDD100K folder.

	└── BDD100K             
	        ├── det_train_only_traffic_light_relevance.json    # training ground truth
	        └── det_val_only_traffic_light_relevance.json      # validation ground truth

The script *merger.py* fuses our additional annotation with the original BDD100K ground truth labels. The script assumes to have the files **det_train.json** and **det_val.json** available in the BDD100K folder and generates the augmented annotation. These generated files remain identical to the original ones, preserving the same structure and content. The only difference is the addition of a new boolean attribute called **trafficLightRelevant**, which is associated with each traffic light entry. This attribute provides information about the relevance of the respective traffic light in its image.

More information about the dataset and the original annotation could be found [HERE](https://www.vis.xyz/bdd100k/). 

# Image labeling
As described in the paper, the problem is formulated as a 3-class image classification task: not-relevant, relevant-green, and relevant-red. To generate the label for each image, the following rule is applied:

All **relevant** traffic lights in the scene with an area greater than a threshold $t$ are selected.
* If all the traffic lights in the selected set display the same color, that color is assigned as the label.
* If the set of colors is {red, unknown} or {green, unknown}, the label is assigned as relevant-red or relevant-green, respectively.
* If the set of colors contains both red and green state, the image is incosistent and, it is discarded.
* If the set is empty, the class label is assigned as not-relevant.

The threshold value $t$ is set to ignore traffic lights with an area smaller than the 20th percentile. This decision was made because these smaller traffic lights are located too far away from the ego vehicle, making it difficult to determine their relevance.

# Authors
- Tomaso Trinci
- Tommaso Bianconcini
- Leonardo Sarti
- Leonardo Taccari
- Francesco Sambo
  
For any issues or problems with the material in this repository, please send an email to tomaso.trinci *at* unifi *dot* it.

# References
If you make use of any material from this repository, please cite
```
@inproceedings{TO BE APPEARED,
  title={Cross-model temporal cooperation via saliency maps for efficient recognition and classification of relevant traffic lights},
  author={Trinci, Tomaso and Bianconcini, Tommaso and Sarti, Leonardo and Taccari, Leonardo and Sambo, Francesco},
  booktitle={2023 IEEE 26rd International Conference on Intelligent Transportation Systems (ITSC)},
  pages={1--6},
  year={2023},
  organization={IEEE}
}
```
# Licence
The data and the source code in this repository are licensed under the MIT license, which you can find in the LICENSE file.
