# FringesPM

Script over python for analysis of fringes on particulate matter with TEM images already in skeleton using top-hat and gaussian filters, finding tortuosity and interplanar distance.

feel free to use it in the name of science.

if you have any advise or wanna colaborate, feel free to put an pull request. it will be great if you can thank me in your work.


## Usage

```python
import fringelabel as fringe

fa = fringe.FringeAnalysis()
fa.load_image("590kx_WF_RD30_07_skeleton.tif")
fa.process_lc()
# fa.process_inter_distance() #Comming soon

```