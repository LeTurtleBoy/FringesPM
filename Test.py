import numpy as np
from skimage import measure, morphology

a = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,2,0,0],[0,0,0,1,0,0,2,0,0],[0,0,1,0,0,0,2,0,0],[0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
a = a.astype(int)
info_image_struct = measure.regionprops(a, coordinates='xy')
for region in info_image_struct:
    aux = np.zeros((len(a), len(a[0])))
    aux.astype(int)
    a.astype(int)
    aux[region.bbox[0]-1:region.bbox[2]+1,region.bbox[1]-1:region.bbox[3]+1] = 1
    image_maskeda = a.copy()
    image_maskeda[aux==0] = 0 
    print(image_masked, a) 

