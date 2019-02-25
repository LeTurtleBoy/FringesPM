import fringelabel as fringe


fa = fringe.FringeAnalysis()
fa.load_image("590kx.tif")
fa.process_lc()
fa.load_inter_distance("590kx.tif")#"590kx_WF_RD30_07_skeleton_final.tif"

"""     
   def process_id(self, mode):
        if mode == "Horizontal":
            I, J = np.nonzero(self.image_h)
            F = [[0, 0, 0]]*len(I)
            for x in range(len(I)):
                F[x]= [self.image_h[I[x]][J[x]],I[x],J[x]]
            df =  pd.DataFrame(F,columns = ['Fringe_label','x','y'])
            print(df.head())
            groups = df.groupby('Fringe_label')
            data_size = len(groups.groups)
            Vector = [0]*data_size
            u = 0
            for ref, df in groups:
                Vector[u] = df.values
                u+=1

            pure_data = []
            n = 0
            for i in range(len(Vector)):
                name = "process fringe " + str(i+1) + " of "+ str(len(Vector)-1) + " possible couples"
                total_it = len(Vector) - i
                pb = ProgressBar(total = total_it, prefix = name,suffix='Ok', decimals=3, length=50, fill='X',zfill='-')
                for j in range(i+1, len(Vector)):
                    pb.print_progress_bar(j-i)
                    l = 0
                    base = Vector[i]
                    aux = Vector[j]
                    for pixinfo in base:
                        aux_data = []
                        old_distance = 0
                        for pixinfo_ in aux:
                            a = pixinfo[1]-pixinfo_[1]
                            b = pixinfo[2]-pixinfo_[2]
                            if a == 0: angle = np.pi/2 * np.sign(b)
                            elif b == 0: angle = np.pi * int(x<0)
                            else: angle = np.arctan(b/a) 
                            angle = angle*(180.0 / np.pi)
                            distance = np.sqrt((a)**2 + (b)**2)
                            if ((distance > 60) | (-45 > angle) | (angle < 45)):
                                break
                            else:
                                if aux_data == []:
                                    aux_data = [pixinfo[0],pixinfo[1],pixinfo[2],pixinfo_[0],pixinfo_[1],pixinfo_[2],distance, angle]
                                    old_distance = distance
                                else:
                                    if distance < old_distance:
                                        aux_data = [pixinfo[0],pixinfo[1],pixinfo[2],pixinfo_[0],pixinfo_[1],pixinfo_[2],distance, angle]
                                        old_distance = distance
                                l-=-1
                        if (aux_data != []):
                            if  pure_data != []:
                                pure_data.append(aux_data)
                            else:
                                pure_data = [aux_data]
                            n-=-1
                pb.print_progress_bar(total_it)
            print("Done")
            a = pd.DataFrame(pure_data)
            a.to_excel("indis.xlsx", index=False)
            print("final i guess?")
"""