import fringelabel as fringe

fa = fringe.FringeAnalysis()
fa.load_image("590kx_WF_RD30_07_skeleton.tif")
fa.process_lc()
# fa.process_inter_distance() #Comming soon