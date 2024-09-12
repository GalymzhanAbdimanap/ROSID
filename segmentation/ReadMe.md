# ROSID Train
This folder contains files for training and testing the ROSID dataset for semantic segmentation.

We used the  [MMSegmentation](https://github.com/open-mmlab/mmsegmentation)  to train the model.

**Step 0.** Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html).

**Step 1.** To train a model on our dataset, you need to install mmsegmentation, here you will find the [installation instructions](https://github.com/open-mmlab/mmsegmentation/blob/master/docs/en/get_started.md). 

**Step 2.** Open the mmsegmentation folder and distribute the files in our repository into folders. 

**Step 3.** Сhange the dataset path in the file ```configs/_base_/datasets/oil_spill_320_320.py``` on your way. 

## Train
