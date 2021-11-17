import json
import os
import dropbox

import csv
from io import StringIO

from api.session import Session
from api.cosmos_db_api import CosmosDBAPI

"""
This class is used to locate sessions on CosmosDB and process the metadata and related files.
This class replaces the obsolete AssessmentAPI class to replace Dropbox dependancy with Azure
"""

class SessionAPI():

    def __init__(self):
        self.dropbox = dropbox.Dropbox(os.environ['DropBox_Key'])
        self.cosmos_db_instance = CosmosDBAPI()

    def get_session(self, session_id):
        session_metadata = self.cosmos_db_instance.get_session(session_id)
        session = Session()
        session.set_metadata(session_metadata)
        return session

    def get_beat_metrics_dropbox(self, session):

        #get dropbox path - to be replaced with azure connection
        full_path = session.get_metadata_property("_dropboxPath")
        version = session.get_metadata_property("schemaVersion")
        
        #HOT FIX for new beats file
        if version == "7.0.0":
            for files in self.dropbox.files_list_folder(full_path).entries:                     
                    if "Beats" in files.name:
                        metadata, response = self.dropbox.files_download(full_path + "/" + files.name)
                        current_file = response.content.decode("utf-8")
                        data = json.loads(current_file)
        else:
            for files in self.dropbox.files_list_folder(full_path).entries:                     
                    if "Metadata" in files.name:
                        metadata, response = self.dropbox.files_download(full_path + "/" + files.name)
                        current_file = response.content.decode("utf-8")
                        data = json.loads(current_file)

        beats = data['beats']

        #Lists to store all the data
        beat_num = []
        centroid_dia_vti = []
        centroid_sys_vti = []
        centroid_total_vti = []
        diastolic_end = []
        diastolic_power = []
        diastolic_vtip = []
        end_systolic_velocity = []
        is_complete = []
        max_sys_vti = []
        max_dia_vti = []
        max_total_vti = []
        peak_systolic_velocity = []
        start_systolic_velocity = []
        systolic_end = []
        systolic_peak = []
        systolic_power = []
        systolic_start = []
        systolic_vtip = []
        time_correctedcycle = []
        time_diastolic = []
        time_systolic = []
        time_totalcycle = []
        total_power = []
        total_vtip = []
        heart_rate = []

        try:
            for beat in beats: 
                beat_num.append(beat['beatNumber'])
                centroid_dia_vti.append(beat['centroidVDiastolicVTI'])
                centroid_sys_vti.append(beat['centroidVSystolicVTI'])
                centroid_total_vti.append(beat['centroidVTotalVTI'])
                diastolic_end.append(beat['diastolicEnd'])
                diastolic_power.append(beat['diastolicPower'])
                diastolic_vtip.append(beat['diastolicVtip'])
                end_systolic_velocity.append(beat['endSystolicVelocity'])
                is_complete.append(beat['isComplete'])
                max_sys_vti.append(beat['maxVSystolicVTI'])
                max_dia_vti.append(beat['maxVDiastolicVTI'])
                max_total_vti.append(beat['maxVTotalVTI'])
                peak_systolic_velocity.append(beat['peakSystolicVelocity'])
                start_systolic_velocity.append(beat['startSystolicVelocity'])
                systolic_end.append(beat['systolicEnd'])
                systolic_peak.append(beat['systolicPeak'])
                systolic_power.append(beat['systolicPower'])
                systolic_start.append(beat['systolicStart'])
                systolic_vtip.append(beat['systolicVtip'])
                time_correctedcycle.append(beat['correctedFlowTime'])
                time_diastolic.append(beat['timeDiastolic'])
                time_systolic.append(beat['timeSystolic'])
                time_totalcycle.append(beat['timeTotal'])
                total_power.append(beat['totalPower'])
                total_vtip.append(beat['totalVtip'])
                heart_rate.append(beat['heartRate'])

            beat_metrics = {
                'beatNum': beat_num,
                'centroidVDiastolicVTI': centroid_dia_vti,
                'centroidVSystolicVTI': centroid_sys_vti,
                'centroidVTotalVTI': centroid_total_vti,
                'diastolicEnd': diastolic_end,
                'diastolicPower': diastolic_power,
                'diastolicVtip': diastolic_vtip,
                'endSystolicVelocity': end_systolic_velocity,
                'isComplete': is_complete,
                'maxVDiastolicVTI': max_dia_vti,
                'maxVSystolicVTI': max_sys_vti,
                'maxVTotalVTI': max_total_vti,
                'peakSystolicVelocity': peak_systolic_velocity,
                'startSystolicVelocity': start_systolic_velocity,
                'systolicEnd': systolic_end,
                'systolicPeak': systolic_peak,
                'systolicPower': systolic_power,
                'systolicStart': systolic_start,
                'systolicVtip': systolic_vtip,
                'correctedFlowTime': time_correctedcycle,
                'timeDiastolic': time_diastolic,
                'timeSystolic': time_systolic,
                'timeTotal': time_totalcycle,
                'totalPower': total_power,
                'totalVtip': total_vtip,
                'heartRate': heart_rate
            }
        #if beats field isn't found or is empty 
        except Exception as e:
            return None

        return beat_metrics

    def get_beat_metrics_json(self, beats_json):
        beats = beats_json['beats']
        
        #Lists to store all the data
        beat_num = []
        centroid_dia_vti = []
        centroid_sys_vti = []
        centroid_total_vti = []
        diastolic_end = []
        diastolic_power = []
        diastolic_vtip = []
        end_systolic_velocity = []
        is_complete = []
        max_sys_vti = []
        max_dia_vti = []
        max_total_vti = []
        peak_systolic_velocity = []
        start_systolic_velocity = []
        systolic_end = []
        systolic_peak = []
        systolic_power = []
        systolic_start = []
        systolic_vtip = []
        time_correctedcycle = []
        time_diastolic = []
        time_systolic = []
        time_totalcycle = []
        total_power = []
        total_vtip = []
        heart_rate = []

        try:
            for beat in beats: 
                beat_num.append(beat['beatNumber'])
                centroid_dia_vti.append(beat['centroidVDiastolicVTI'])
                centroid_sys_vti.append(beat['centroidVSystolicVTI'])
                centroid_total_vti.append(beat['centroidVTotalVTI'])
                diastolic_end.append(beat['diastolicEnd'])
                diastolic_power.append(beat['diastolicPower'])
                diastolic_vtip.append(beat['diastolicVtip'])
                end_systolic_velocity.append(beat['endSystolicVelocity'])
                is_complete.append(beat['isComplete'])
                max_sys_vti.append(beat['maxVSystolicVTI'])
                max_dia_vti.append(beat['maxVDiastolicVTI'])
                max_total_vti.append(beat['maxVTotalVTI'])
                peak_systolic_velocity.append(beat['peakSystolicVelocity'])
                start_systolic_velocity.append(beat['startSystolicVelocity'])
                systolic_end.append(beat['systolicEnd'])
                systolic_peak.append(beat['systolicPeak'])
                systolic_power.append(beat['systolicPower'])
                systolic_start.append(beat['systolicStart'])
                systolic_vtip.append(beat['systolicVtip'])
                time_correctedcycle.append(beat['correctedFlowTime'])
                time_diastolic.append(beat['timeDiastolic'])
                time_systolic.append(beat['timeSystolic'])
                time_totalcycle.append(beat['timeTotal'])
                total_power.append(beat['totalPower'])
                total_vtip.append(beat['totalVtip'])
                heart_rate.append(beat['heartRate'])

            beat_metrics = {
                'beatNum': beat_num,
                'centroidVDiastolicVTI': centroid_dia_vti,
                'centroidVSystolicVTI': centroid_sys_vti,
                'centroidVTotalVTI': centroid_total_vti,
                'diastolicEnd': diastolic_end,
                'diastolicPower': diastolic_power,
                'diastolicVtip': diastolic_vtip,
                'endSystolicVelocity': end_systolic_velocity,
                'isComplete': is_complete,
                'maxVDiastolicVTI': max_dia_vti,
                'maxVSystolicVTI': max_sys_vti,
                'maxVTotalVTI': max_total_vti,
                'peakSystolicVelocity': peak_systolic_velocity,
                'startSystolicVelocity': start_systolic_velocity,
                'systolicEnd': systolic_end,
                'systolicPeak': systolic_peak,
                'systolicPower': systolic_power,
                'systolicStart': systolic_start,
                'systolicVtip': systolic_vtip,
                'correctedFlowTime': time_correctedcycle,
                'timeDiastolic': time_diastolic,
                'timeSystolic': time_systolic,
                'timeTotal': time_totalcycle,
                'totalPower': total_power,
                'totalVtip': total_vtip
            }
        #if beats field isn't found or is empty 
        except Exception as e:
            return None

        return beat_metrics
        

    def get_iq_data(self, session):
        #get dropbox path - to be replaced with azure connection
        full_path = session.get_metadata_property("_dropboxPath")
    
        for files in self.dropbox.files_list_folder(full_path).entries:                
                
            if "IQData" in files.name:
                metadata, response = self.dropbox.files_download(full_path + "/" + files.name)
                try:
                    current_file = response.content.decode("utf-8")
                    print("Detected uncompressed IQ file")
                    return current_file
                except UnicodeDecodeError as e:
                    print("Detected compressed IQ file")
                    return response.content
                        
        return None       

    def get_tick_data(self, session):
        #get dropbox path - to be replaced with azure connection
        full_path = session.get_metadata_property("_dropboxPath")
    
        for files in self.dropbox.files_list_folder(full_path).entries:                
               
            if "TickData" in files.name:
                metadata, response = self.dropbox.files_download(full_path + "/" + files.name)
                current_file = response.content.decode("utf-8")
                return current_file

        return None
        
    def get_raw_data(self, session):
        #get dropbox path - to be replaced with azure connection
        full_path = session.get_metadata_property("_dropboxPath")
    
        for files in self.dropbox.files_list_folder(full_path).entries:                
            if "RawData" in files.name:
                metadata, response = self.dropbox.files_download(full_path + "/" + files.name)
                current_file = response.content.decode("utf-8")
                return current_file

        return None         
                            
    def get_dropped_packets(self, session):
        #get dropbox path - to be replaced with azure connection
        full_path = session.get_metadata_property("_dropboxPath")
    
        for files in self.dropbox.files_list_folder(full_path).entries:                
            if "DroppedPackets" in files.name:
                metadata, response = self.dropbox.files_download(full_path + "/" + files.name)
                current_file = response.content.decode("utf-8")
                return current_file

        return None

    def JSON_to_CSV(self, beats_json):
        try:
            sample_period = beats_json["samplePeriod"]
            if sample_period is not None:
                sample_period *= 1000.0
                del beats_json['samplePeriod']
            else:
                print("There was an error while creating the beats CSV file. Sample rate could not be loaded")
                return None

            field_names = ['Beat Number', 'Systolic Start', 'Systolic Peak', 'Systolic End', 'Diastolic End',
                           'Artifact', 'Descriptor']

            # Open a csv file in memory and write the beats
            buffer = StringIO()
            writer = csv.DictWriter(buffer, fieldnames=field_names)
            writer.writeheader()

            for i in range(len(beats_json['beatNum'])):
                writer.writerow({'Beat Number': beats_json['beatNum'][i] + 1,
                                 'Systolic Start': round((beats_json['systolicStart'][i] - 54) * sample_period),
                                 'Systolic Peak': round((beats_json['systolicPeak'][i] - 54) * sample_period),
                                 'Systolic End': round((beats_json['systolicEnd'][i] - 54) * sample_period),
                                 'Diastolic End': round((beats_json['diastolicEnd'][i] - 54) * sample_period)})

            buffer.seek(0)
            return buffer

        except Exception as e:
            print("There was an error while creating the beats CSV file")
            print(e)
            return None


    

