# ROSID Train
This folder contains files for training and testing the ROSID dataset for semantic segmentation.

We used the  [MMSegmentation](https://github.com/open-mmlab/mmsegmentation)  to train the model.

**Step 0.** Download and install Miniconda from the [official website](https://docs.conda.io/en/latest/miniconda.html).

**Step 1.** To train a model on our dataset, you need to install mmsegmentation, here you will find the [installation instructions](https://github.com/open-mmlab/mmsegmentation/blob/master/docs/en/get_started.md). 

**Step 2.** Open the mmsegmentation folder and distribute the files in our repository into folders. 

## Preprocessing
**Step 3.** The dataset is divided into 320x320 pixel fragments with stride 106px.
```shell
python create_data_320_320.py
```

**Step 4.** Сhange the dataset path in the file ```configs/_base_/datasets/oil_spill_320_320.py``` on your way which you will receive as a result of previous step. 

## Train
```shell
python tools/train.py configs/mask2former/mask2former_r50_8xb2-90k_cityscapes-512x1024.py
```

## Test
```shell
python tools/test.py configs/mask2former/mask2former_r50_8xb2-90k_cityscapes-512x1024.py work_dirs\mask2former_r50_8xb2-90k_cityscapes-512x1024\iter_40000.pth
```



