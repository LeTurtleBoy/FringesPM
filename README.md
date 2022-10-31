# FringesPM

Script over python for analysis of fringes on particulate matter with TEM images already in skeleton using top-hat and gaussian filters, finding tortuosity and interplanar distance.

feel free to use it in the name of science.



## Usage

```python
from modules.fringelabel import FringeAnalysis
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


fringe = FringeAnalysis()
fringe.load_image("Images/Process/590kx_WF_RD30_07_skeleton_Filtrado.tif")
fringe.process_lc()

```
### requirements:
- cv2
- numpy
- skimage
- PIL
- pandas
- console_progressbar 

#### installing requirements:

```
pip install -r requirements.txt
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
It will be great if you can thank me in your work.
