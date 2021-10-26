#An extraction tool for converting MC data into format suitable for hitman

#To use this function just call the script and the number of the root file at the end
#e.g. $extract.py -i a_simulation.root -o converted.pkl

def main():
    import argparse

        #Get command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_files', help='Type = String; Input locations of training set files, e.g. $PWD/simfiles.root.', nargs='+', required=True)
    parser.add_argument('-o', '--output_file', help='Type = String; Output location for converted data, e.g. $PWD/combined_set.pkl', nargs=1, required=True)
    args = parser.parse_args()

    from rat2py import snake
    import numpy as np
    import sys
    import pickle
    import math

    #warning! doesnt check particle ID!

    min_pmt_hits=4
    events=[]
    labels=['x','y','z','zenith','azimuth','t','energy']
    sn = snake()
    event_range=[]
    file_num=0
    for sourcefile in args.input_files:
        sn.openFile(sourcefile)
        
        for event in range(0,sn.getEntries()):
            sn.getEvent(event)
            charges, times ,noise = sn.getHitInfo()
            PMT_id=sn.getID()
            pmts=np.where(charges>-100)[0] #get index of nonzero values
            if (len(pmts) > 0 and len(np.where(PMT_id[pmts]==1)[0]) >= min_pmt_hits):
                sn.getMCTruth()
                x,y,z=sn.getXYZ()
                p=np.column_stack(sn.getMCVal())
                zenith = math.acos(p[0,5]/np.linalg.norm(p[0,3:6],2))
                azimuth = math.atan2(p[0,4], p[0,3])
                if azimuth < 0:
                    azimuth = azimuth + 2*np.pi
                p=np.column_stack((p[0,0],p[0,1],p[0,2],zenith,azimuth,p[0,6],p[0,7]))
                new_params = np.repeat(p, len(pmts), axis=0)
                new_hits = np.column_stack((x[pmts],y[pmts],z[pmts],times[pmts],charges[pmts],PMT_id[pmts],noise[pmts]))

                data={
                    "hits":  new_hits,
                    "total_charge": [np.sum(new_hits[:,4]),len(new_hits)],
                    "truth": p[0]   
                }
                events.append(data)
            if(event%5000==0):
                print(sourcefile+": "+str(100*event/sn.getEntries())+"% complete.")
                print("-----------------------------------------------------------")
        file_num+=1
        print("File " + str(file_num) + " of " + str(len(args.input_files)) + " complete")


    fileObj = open(args.output_file[0], 'wb')
    pickle.dump(events,fileObj)
    fileObj.close()
