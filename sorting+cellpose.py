# import library
import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os
from pathlib import Path

# Input: Path for original image files
for x in os.listdir("D:/Images/Running list"):
    path1 = "D:/Images/Running list"
    path2 = x
    path3 = "TimePoint_1/"
    fullpath1 = os.path.join(path1,path2)
    fullpath2 = os.path.join(fullpath1,path3)
    main_folder = Path(fullpath2)

    # Create new folder "Masks"
    Path(Path.joinpath(main_folder,"Masks")).mkdir(exist_ok=True)

    # group images for wavelength 1 (nuclei image) & wavelength 4 (phase-contrast image)
    from natsort import natsorted
    filelist1 = natsorted(main_folder.glob("*_w1*"))
    filelist2 = natsorted(main_folder.glob("*_w4*"))

    # Run cellpose for groups for w1 and w4
    from cellpose.models import Cellpose
    for i in range(len(filelist1)):
        image1 = tifffile.imread(filelist1[i])
        image2 = tifffile.imread(filelist2[i])
        model = Cellpose(gpu=True, model_type="cyto2")
        out = model.eval(np.array([image1, image2]), channels=[2,1], channel_axis=0, diameter=40, cellprob_threshold=-4, min_size=15, flow_threshold=1)

    # save the mask in the original path where original images are
        image_path=Path(filelist2[i])
        mask_name=image_path.parent.joinpath(image_path.stem+"_mask.tif")
        tifffile.imsave(mask_name, out[0])

        # group created mask images
    from pathlib import PurePath
    filelist3 = natsorted(main_folder.glob("*_mask.TIF"))

    # move created mask images to new folder "Masks"
    for j in range(len(filelist3)):
        orig_path = Path(filelist3[j])
        path_list = list(PurePath(orig_path).parts)
        path_list.insert(5, "Masks")
        new_path = PurePath("").joinpath(*path_list)
        Path(orig_path).rename(new_path)
