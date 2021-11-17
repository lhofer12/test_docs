import statistics as stat
import numpy as np
from api.session_api import SessionAPI
from api.cosmos_db_api import CosmosDBAPI

class thresholdCalc():
    def __init__(self):
        self.sessionapi = SessionAPI()
    
    def calc_metrics(self,session_id):
        print('calc here')
        session = self.sessionapi.get_session(session_id)
        print('calc here2')
        session_beats = self.sessionapi.get_beat_metrics_dropbox(session)
        print('calc here 3')
        # list so easier to work with:
        beat_num = session_beats["beatNum"]
        diastolic_end = session_beats["diastolicEnd"]
        systolic_end = session_beats["systolicEnd"]
        systolic_peak = session_beats["systolicPeak"]
        systolic_start = session_beats["systolicStart"]
        time_correctedcycle = session_beats["correctedFlowTime"]
        heart_rate = session_beats["heartRate"]

        # define empty arrays 
        SP_fraction = [0]*len(beat_num)         # SP fraction array length of num_beats
        SE_fraction = [0]*len(beat_num)         # SE fraction array length of num_beats
        to_remove = []                          # empty array for removing negative SE values after

        # find SP and SE fractions for each beat
        for i in range(0,len(beat_num)):
            SP_fraction[i] = (systolic_peak[i]-systolic_start[i])/(diastolic_end[i]-systolic_start[i])
            SE_fraction[i] = (systolic_end[i]-systolic_start[i])/(diastolic_end[i]-systolic_start[i])
            if (SE_fraction[i]<0): 
                SE_fraction[i] = None
                to_remove.append(i)

        SE_fraction = list(filter(None,SE_fraction))            # remove negative SE values

        # print(time_correctedcycle)
        # calculate metrics
        CV_CCFT = stat.stdev(time_correctedcycle)/stat.mean(time_correctedcycle)
        CV_SP = stat.stdev(SP_fraction)/stat.mean(SP_fraction)
        CV_SE = stat.stdev(SE_fraction)/stat.mean(SE_fraction)
        COD_CCFT = (np.percentile(time_correctedcycle,75)-np.percentile(time_correctedcycle,25))/(np.percentile(time_correctedcycle,75)+np.percentile(time_correctedcycle,25))
        COD_SP = (np.percentile(SP_fraction,75)-np.percentile(SP_fraction,25))/(np.percentile(SP_fraction,75)+np.percentile(SP_fraction,25))
        COD_SE = (np.percentile(SE_fraction,75)-np.percentile(SE_fraction,25))/(np.percentile(SE_fraction,75)+np.percentile(SE_fraction,25))
        CV_HR = stat.stdev(heart_rate)/stat.mean(heart_rate)

        metrics = {
            "CV_CCFT": CV_CCFT, 
            "CV_SP": CV_SP,
            "CV_SE": CV_SE,
            "COD_CCFT": COD_CCFT,
            "COD_SP": COD_SP, 
            "COD_SE": COD_SE,
            "CV_HR": CV_HR
        }
        
        session_metadata = CosmosDBAPI().get_session(session_id) 
        session_metadata['metrics'] = metrics
        CosmosDBAPI().update_session(session_metadata)
        
        return metrics
    
    def threshold_metrics(self, metrics):
        ### set thresholds here
        thresholds = {
            "CV_CCFT": 0.15, 
            "CV_SP": None,
            "CV_SE": None,
            "COD_CCFT": 0.065,
            "COD_SP": 0.11, 
            "COD_SE": 0.089,
            "CV_HR": None
        }
        crossing = []
        # find metrics that cross thresholds and return
        for item in metrics: 
            if (thresholds[item] != None):
                if (metrics[item] > thresholds[item]):
                    crossing.append(item)
        return crossing

        