from modules.fringelabel import FringeAnalysis
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


fringe = FringeAnalysis()
fringe.load_image("Images/Process/590kx_WF_RD30_07_skeleton_Filtrado.tif")
fringe.process_lc()

