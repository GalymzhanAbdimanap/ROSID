from mmseg.registry import DATASETS
from .basesegdataset import BaseSegDataset

@DATASETS.register_module()
class OilSpillDataset(BaseSegDataset):
  METAINFO = dict(
        classes=('oil', 'cloud', 'shadow', 'water', 'urban', 'soil', 'vegetation', 'look_a_like', 'background'),
        palette=[[255, 0, 0],[255, 255, 255],[128, 128, 128],[0, 255, 255],[255, 0, 255], [128, 64, 48], [0, 255, 0], [255, 215, 0], [95,220,194]])

  def __init__(self, split, **kwargs):
    super().__init__(img_suffix='.png', seg_map_suffix='.png', 
                     ann_file=split, **kwargs)
