# -*- coding: utf-8 -*-
from math import floor

"""The Integrated Analysis module for the metadata-drive dashcam"""
import os
import sqlite3
import argparse
import re
import json
from dateutil.parser import parse

DEVICE_ID = 1;

""" type_list"""
FRONT = 1; REAR = 2; DUAL = 3;

""" metadata_type """
UNKNOWN = 1; CHUNK = 10; CHUNK_NAME = 11; CHUNK_SEQUENCE = 12;
DEVICE = 20; MODEL=21; VERSION=22; CHANNEL=23; LOCATION=30
RECORD_MODE = 40; EVENT = 41; MANUAL = 42; NORMAL = 43; PARKING=44;
STATUS = 50; G_SENSOR = 51; SPEED = 52; VOLTAGE = 53;
TIME = 60; TIME_CREATED = 61; TIME_MODIFIED = 62; DATE_ACCESSED = 63; DATE_CREATED = 64
USER_PREFERENCE = 70; FRAME_PER_SECOND = 71; LANGUAGE = 72; PROFILE_LEVEL = 73; RESOLUTION = 74; TIMEZONE = 75;

""" metadata_source """
DIRECTORY_NAME = 11; FILE_NAME = 12; D_TIMESTAMP = 13;
MULTIMEDIA = 20; LIST_OF_CHUNKS = 21; META_CHUNKS = 22; STREAM_CHUNKS = 23; VIDEO_STREAM = 24; SUBTITLE_STREAM = 25;
OTHER_FILES = 40; NMEA = 41; CUSTOM_BINARY = 42;

class _GPRMC:
    def __init__(self):
        self.sentenceid = None
        self.utc_time = None
        self.status = None
        self.latitude = None
        self.indicator_ns = None
        self.longtitude = None
        self.indicator_ew = None
        self.speed = None
        self.course = None
        self.utc_date = None
        self.magnetic = None
        self.checksum = None
        self.convert_time = None

class _FILE:
    file_dict = {}
    def __init__(self):
        self.file_dict = {}

class _DIR:
    dir_dict = {}
    def __init__(self):
        self.dir_dict = {}

class _DEVICE_INFO:
    def __init__(self):
        self.manufacture = None
        self.model = None
        self.version = None
        self.filesystem = None
        self.cam_channel = None
        self.container_format = None
        self.location_type = None
        self.filenameing_rule = None
        self.timezone = None
        self.language = None
    def INT(self):
        self.cam = 0

class DashcamMetadataDatabase:
    _filename_idx = 0
    _dir_idx = 1
    _metadata_idx = 0

    def __init__(self):
        self._connection = None
        self._cursor = None
        self._filename = None

    def set_filename(self, filename):
        self._filename = filename

    def database_open(self):
        if not self._filename:
            raise ValueError('Missing filename.')
        self._connection = sqlite3.connect(self._filename)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    """Create Integrated Analysis Result Database"""
    def initialize_database_file(self):
        self._cursor.execute(
            'CREATE TABLE if not exists device_info( device_id INT NOT NULL UNIQUE, manufacture TEXT NOT NULL, model TEXT NOT NULL, '
            'version TEXT NOT NULL, filesystem TEXT NOT NULL, cam_channel INT NOT NULL, container_format INT NOT NULL, '
            'location_type INT NOT NULL, filenaming_rule TEXT NOT NULL, timezone TEXT NOT NULL, language TEXT NOT NULL) ')
        self._connection.commit()

        #CREATE directory_info
        self._cursor.execute(
            'CREATE TABLE if not exists directory_info(dir_id INT NOT NULL UNIQUE, device_id INT NOT NULL, dir_info TEXT NOT NULL,'
            'dir_name TEXT NOT NULL, dir_path TEXT NOT NULL, is_deleted BOOL NOT NULL)')
        self._connection.commit()

        # CREATE file_info
        self._cursor.execute(
            'CREATE TABLE if not exists file_info(file_id INT NOT NULL UNIQUE, dir_id INT NOT NULL, file_name TEXT NOT NULL, file_type INT NOT NULL,'
            'is_deleted BOOL NOT NULL, is_recover BOOL NOT NULL, is_rawdata BOOL NOT NULL, rawdata BLOB NOT NULL, file_path TEXT NOT NULL)')
        self._connection.commit()

        # CREATE metadata
        self._cursor.execute(
            'CREATE TABLE if not exists metadata(rec_id INT NOT NULL UNIQUE, file_id INT NOT NULL, data_source INT NOT NULL, data_type INT NOT NULL,'
            'std_time TEXT NOT NULL, data2_value TEXT NOT NULL, data3_value BLOB NOT NULL )')
        self._connection.commit()

        # CREATE metadata_src_list
        self._cursor.execute('CREATE TABLE if not exists metadata_src_list(meta_src_no INT NOT NULL UNIQUE, metadata_src_name TEXT NOT NULL)')
        self._connection.commit()

        # CREATE type_list
        self._cursor.execute('CREATE TABLE if not exists metadata_type_list(type_no INT NOT NULL UNIQUE, name TEXT NOT NULL)')
        self._connection.commit()

        # CREATE type_list
        self._cursor.execute('CREATE TABLE if not exists type_list(type_no INT NOT NULL UNIQUE, name TEXT NOT NULL)')
        self._connection.commit()

        # CREATE time_value
        self._cursor.execute(
            'CREATE TABLE if not exists time_value(rec_id INT NOT NULL UNIQUE, file_id INT NOT NULL, data_source INT NOT NULL,'
            'data_type INT NOT NULL, time_value TEXT NOT NULL, utc_time INT NOT NULL)')
        self._connection.commit()

    def insert_default_data(self):
        self._cursor.execute(
            'INSERT INTO metadata_type_list values(1, \'unknown\'), (10, \'CHUNK\'), (11, \'chunk_name\'), (12, \'chunk_sequence\'),' \
            '(20, \'DEVICE\'), (21, \'model\'), (22, \'version\'), (23, \'channel\'), (30, \'location\'),' \
            '(40, \'RECORD_MODE\'), (41, \'event\'), (42, \'manual\'), (43, \'normal\'), (44, \'parking\'),' \
            '(50, \'STATUS\'), (51, \'g-sensor\'), (52, \'speed\'), (53, \'voltage\'),' \
            '(60, \'TIME\'), (61, \'time_created\'), (62, \'time_modified\'), (63, \'date_accessed\'), (64, \'date_created\'),' \
            '(70, \'USER_PREFERENCE\'), (71, \'frame_per_second\'), (72, \'language\'), (73, \'profile_level\'), (74, \'resolution\'),(75, \'timezone\')'
        )
        self._connection.commit()
        self._cursor.execute(
            'INSERT INTO metadata_src_list values(1, \'unknown\'), (10, \'FILESYSTEM\'), (11, \'directory_name\'), (12, \'file_name\'), (13, \'timestamp\'), (14, \'unallocated_area\'),' \
            '(20, \'MULTIMEDIA\'), (21, \'list_of_chunks\'), (22, \'meta_chunks\'), (23, \'stream_chunks\'), (24, \'video_steam\'),' \
            '(25, \'subtitle_stream\'), (26, \'decoding_nal\'), (27, \'sei_nal\'), (28, \'decoded_video_frame\'), (29, \'free_chunks\'),' \
            '(40,  \'OTHER_FILES\'), (41, \'nmea\'), (42, \'custom_binary\'), (43, \'user_preferences\')'
        )
        self._connection.commit()

    def set_device_info(self, Device_info):
        query = 'INSERT INTO device_info VALUES({0:d},"{1:s}","{2:s}","{3:s}","{4:s}",{5:d},{6:d},{7:d},"{8:s}","{9:s}","{10:s}")'\
            .format(1, Device_info.manufacture, Device_info.model, Device_info.version, Device_info.filesystem, Device_info.cam_channel,
                    Device_info.container_format,   Device_info.location_type, Device_info.filenameing_rule,  Device_info.timezone, Device_info.language)
        self._cursor.execute(query)
        self._connection.commit()

    #def get_metadata_from_dir(self, data):

    """ METADATA SOURCE: Directory Name | File Name | Directory / File Timestamp """
    def work_filesystem(self, datas):
        for data in datas:
            # FILE LIST
            if data['inode'] not in _FILE.file_dict:
                dir_id = 0
                _FILE.file_dict[data['inode']] = data['filename']
                """ IAR: DIR_INFO """
                if os.path.dirname(data['filename']) not in _DIR.dir_dict:
                    _DIR.dir_dict[os.path.dirname(data['filename'])] = self._dir_idx
                    dir_id = self._dir_idx
                    # insert directory_info
                    self.insert_dir_info(self._dir_idx, DEVICE_ID, 'not yet', os.path.dirname(data['filename']), 'not yet', False)

                    # T
                    time_data = self.get_time_from_string(os.path.dirname(data['filename']))
                    if not time_data == UNKNOWN:
                        self.insert_metdata(dir_id, DIRECTORY_NAME, DATE_CREATED, 'not yet', time_data, 0)

                    # R
                    record_data = self.get_recordmode_from_string('DIR', os.path.dirname(data['filename']))
                    if not record_data == UNKNOWN:
                        self.insert_metdata(int(data['inode']), DIRECTORY_NAME, record_data[0], 'not yet', record_data[1], 1)

                    self._dir_idx += 1
                else:
                    dir_id = _DIR.dir_dict[os.path.dirname(data['filename'])]

                """ IAR: FILE_INFO """
                # insert file_info
                self.insert_file_info(int(data['inode']), dir_id, os.path.basename(data['filename']), 1, False, False, False, 1, data['filename'])

                ext = str(data['filename'])
                ext = os.path.splitext(os.path.splitext(ext)[1][1:])[0]
                if ext.lower() in ('mp4', 'avi'):  # for mp4 / avi file
                    # R
                    _meta_recordmode = self.get_recordmode_from_string('FILE', os.path.basename(data['filename']))
                    if not _meta_recordmode == 0:
                        self.insert_metdata(int(data['inode']), FILE_NAME, _meta_recordmode[0], 'not yet', _meta_recordmode[1], 1)

                    # D-ch
                    dc = self.device_channel(os.path.basename(data['filename']))
                    if not dc == UNKNOWN:
                        self.insert_metdata(int(data['inode']), FILE_NAME, CHANNEL, 'not yet', dc, 1)

                    # T
                    _meta_time = self.get_time_from_string(data['filename'])
                    if not _meta_time == UNKNOWN:
                    #if len(_meta_time) > 0:
                        self.insert_metdata(int(data['inode']), FILE_NAME, TIME_CREATED, str(_meta_time), str(_meta_time), 1)

            """ METADATA SOURCE = DIRECTORY / FILE TIMESTAMP"""
            """ METADATA TYPE : Time """
            print(data['inode'],  data['MACB'], data['filename'], data['datetime'])
            self.insert_metdata(int(data['inode']), D_TIMESTAMP, self.plaso_time_value(data['MACB']), data['datetime'], data['datetime'], 1)
            #self.insert_time_value(int(data['inode']), D_TIMESTAMP, self.plaso_time_value(data['MACB']), data['datetime'], 0)

    """ METADATA SOURCE: MULTIMEDIA """
    """ METADATA TYPE: LIST OF CHUNKS """
    def work_multimedia(self, datas):
        if len(datas) > 0:
            for data in datas:
                # C
                temp = data['description'].split(" : ")
                self.insert_metdata(int(data['inode']), LIST_OF_CHUNKS, CHUNK_SEQUENCE, 'not yet', temp[1], 1)

    """ METADATA SOURCE: MULTIMEDIA """
    """ METADATA TYPE: META_CHUNKS """
    def work_metachunks(self, datas):
        if len(datas) > 0:
            for data in datas:
                # T - tc
                create_value = self.get_metadata_from_metachunks(TIME_CREATED, data['description'])
                if not create_value == UNKNOWN:
                    self.insert_metdata(int(data['inode']), META_CHUNKS, TIME_CREATED, create_value, create_value, 1)

                # T - tm
                time_value = self.get_metadata_from_metachunks(TIME_MODIFIED, data['description'])
                if not time_value == UNKNOWN:
                    self.insert_metdata(int(data['inode']), META_CHUNKS, TIME_MODIFIED, time_value, time_value, 1)

                # U - fs
                data_value = self.get_metadata_from_metachunks(RESOLUTION, data['description'])
                if not data_value == UNKNOWN:
                    self.insert_metdata(int(data['inode']), META_CHUNKS, RESOLUTION, str(create_value), data_value, 1)

                # U - re
                fps_Value = self.get_metadata_from_metachunks(FRAME_PER_SECOND, data['description'])
                if not fps_Value == UNKNOWN:
                    self.insert_metdata(int(data['inode']), META_CHUNKS, FRAME_PER_SECOND, str(create_value), fps_Value, 1)

    """ METADATA SOURCE: MULTIMEDIA """
    """ METADATA TYPE: SUBTITLE_STREAM """
    # subtitle_stream : b'gsensori,4,512,-01,-130,-18;CAR,0,0,0,0.0,0,0,0,0,0,0,0,0\x00\x00'
    # subtitle_stream : b'gsensori,4,512,-01,-129,011;GPRMC,051949.00,A,3728.770523,N,12721.884153,E,0.0,280.3,030819,6.1,W,A*24\r\r\n;CAR,0,0,0,0.0,0,0,0,0,0,0,0,0\x00\x00'
    def work_subtitle(self, datas):
        if len(datas) > 0:
            for data in datas:
                temps = str(data['description']).split(";")
                for temp in temps:
                    std_time = 'not yet'
                    # S-gs
                    if 'gsensori' in temp:
                        gsensor = self.get_metadata_from_subtitle(G_SENSOR, temp)
                        self.insert_metdata(int(data['inode']), SUBTITLE_STREAM, G_SENSOR, std_time, gsensor, 1)
                    # L / T-tc / S-sp
                    if 'GPRMC' in temp:
                        temp_gprmc = _GPRMC()
                        temp_gprmc = self.get_metadata_from_subtitle(LOCATION, temp)
                        self.insert_metdata(int(data['inode']), SUBTITLE_STREAM, LOCATION, str(temp_gprmc.convert_time), str(temp_gprmc.latitude)+","+str(temp_gprmc.longtitude), 1) #LOCATION
                        self.insert_metdata(int(data['inode']), SUBTITLE_STREAM, SPEED, str(temp_gprmc.convert_time), str(temp_gprmc.speed)+" km/h", 1) #SPEED

    def get_metadata_from_subtitle(self, type, data):
        rtrValue = 'unknown'
        if type == G_SENSOR:
            if '$GSENSOR' in data: # NMEA : $GSENSOR,-219,-174,421
                gsensor_data = str(data).split(",")
                rtrValue = gsensor_data[1] +","+ gsensor_data[2] +","+ gsensor_data[3]
            else: # subtitle_stream : b'gsensori,4,512,-01,-130,-18;CAR,0,0,0,0.0,0,0,0,0,0,0,0,0\x00\x00'
                gsensor_data = str(data).split(",")
                rtrValue = gsensor_data[3] +","+ gsensor_data[4] +","+ gsensor_data[5]
        elif type == LOCATION:
            rtrValue = self.get_metadata_from_GPRMC(data)

        return rtrValue

    def work_other_filies(self, work_source, datas):
        WORK_SOURCE = work_source
        if len(datas) > 0:
            for data in datas:
                temps = str(data['description']).split(" : ")
                std_time = 'not yet'
                # S-gs
                if 'GSENSOR' in temps[1]:
                    gsensor = self.get_metadata_from_subtitle(G_SENSOR, temps[1])
                    self.insert_metdata(int(data['inode']), WORK_SOURCE, G_SENSOR, data['datetime'], gsensor, 1)
                # L, S-sp
                #elif 'GPRMC' or 'GNRMC' in temps[1]:
                elif 'GPRMC' in temps[1]:
                    temp_gprmc = _GPRMC()
                    temp_gprmc = self.get_metadata_from_subtitle(LOCATION, temps[1])
                    self.insert_metdata(int(data['inode']), WORK_SOURCE, LOCATION, str(temp_gprmc.convert_time),
                                        str(temp_gprmc.latitude) + "," + str(temp_gprmc.longtitude), 1)  # LOCATION
                    self.insert_metdata(int(data['inode']), WORK_SOURCE, SPEED, str(temp_gprmc.convert_time),
                                        str(temp_gprmc.speed) + " km/h", 1)  # SPEED
                # S-sp
                elif 'SPEED' in temps[1]: # custom_binary : SPEED, 0
                    split_data = temps[1].split(",")
                    self.insert_metdata(int(data['inode']), WORK_SOURCE, SPEED, data['datetime'],
                                        str(split_data[1]) + " km/h", 1)  # SPEED
                # L
                elif 'LOCATION' in temps[1]: # custom_binary : LOCATION, 37351756, 127015432, 5
                    split_data = temps[1].split(",")
                    self.insert_metdata(int(data['inode']), WORK_SOURCE, LOCATION, data['datetime'],
                                        str(split_data[1]) + "," + str(split_data[2]), 1)  # LOCATION

    def get_metadata_from_GPRMC(self, data):
        rtrData = _GPRMC()

        split_data = data.split(",")
        rtrData.sentenceid = split_data[0]
        rtrData.utc_time = split_data[1]
        rtrData.status = split_data[2]
        rtrData.latitude = split_data[3]
        rtrData.indicator_ns = split_data[4]
        rtrData.longtitude = split_data[5]
        rtrData.indicator_ew = split_data[6]
        rtrData.speed = split_data[7]
        rtrData.course = split_data[8]
        rtrData.utc_date = split_data[9]
        rtrData.magnetic = split_data[10]
        rtrData.checksum = split_data[11]

        hours = int(split_data[1][0:2])
        minutes = int(split_data[1][2:4])
        seconds = float(split_data[1][4:])
        day = int(split_data[9][0:2])
        month = int(split_data[9][2:4])
        year = 2000 + int(split_data[9][4:6])
        temp = self.dd2dms(rtrData.latitude,  rtrData.indicator_ns)
        temp2 = self.dd2dms(rtrData.longtitude, rtrData.indicator_ew)
        rtrData.convert_time = parse(str(year) +"-"+str(month) +"-"+str(day) +" "+str(hours) +":"+str(minutes) +":"+str(seconds))
        return rtrData

    def dd2dms(self, decimaldegree, direction='x'):
        if type(decimaldegree) != 'float':
            try:
                decimaldegree = float(decimaldegree)
            except:
                print('\nERROR: Could not convert %s to float.' % (type(decimaldegree)))
                return 0
        if decimaldegree < 0:
            decimaldegree = -decimaldegree
            if direction == 'x':
                appendix = 'W'
            else:
                appendix = 'S'
        else:
            if direction == 'x':
                appendix = 'E'
            else:
                appendix = 'N'
        minutes = decimaldegree % 1.0 * 60
        seconds = minutes % 1.0 * 60

        return '{0}°{1}\'{2:2.3f}"{3}'.format(int(floor(decimaldegree)), int(floor(minutes)), seconds, appendix)

    def get_metadata_from_metachunks(self, type, data):
        #MP4 : meta_chunks : {'version': 0, 'flags': '0x000000', 'creation_time': '2019-08-03 05:19:49', 'modification_time': '2019-08-03 05:19:49', 'timescale': 24000, 'duration': 0, 'language': '0x00'}
        rtrValue = UNKNOWN
        try:
            temp = str(data).replace("'", "\"")
            temp = temp.split(" : ")
            json_data = json.loads(temp[1])


            if type == TIME_CREATED:
                if 'creation_time' in json_data:
                    rtrValue = json_data['creation_time']
                elif 'ICRD' in json_data:
                    rtrValue = json_data['ICRD']
            elif type == TIME_MODIFIED:
                if 'modification_time' in json_data:
                    rtrValue = json_data['modification_time']
            elif type == RESOLUTION:
                if 'width' in json_data and 'height' in json_data and json_data['track_ID'] == 1:
                    rtrValue = str(json_data['width']) + "x" + str(json_data['height'])
                elif 'dwWidth' in json_data and 'dwHeight' in json_data:
                    rtrValue = str(json_data['dwWidth']) + "x" + str(json_data['dwHeight'])
            elif type == FRAME_PER_SECOND:
                if 'rate' in json_data:
                    rtrValue = str(json_data['duration']/json_data['timescale']) + ' FPS'
                elif 'dwRate' in json_data:
                    rtrValue = str(json_data['dwRate']) + ' FPS'
            else:
                rtrValue = UNKNOWN
            return rtrValue
        except:
            return rtrValue

    def get_time_from_string(self, data):
        _time = None
        pattern1 = re.compile(r'\d{8}[\-|\_|]\d{6}')
        pattern2 = re.compile(r'\d{4}[\-|\_|]\d{2}[\-|\_]\d{2}[\-|\_]\d{2}[\-|\_]\d{2}[\-|\_]\d{2}')
        pattern3 = re.compile(r'\d{8}')
        #YYYY-MM-DD hh:mm:ss

        p1 = pattern1.search(data)
        p2 = pattern2.search(data)
        p3 = pattern3.search(data)
        if p1:  #YYYYMMDD-hhmmss(- or _)
            _time = p1.group()
        elif p2:    #YYYY-MM-DD-hh-mm-ss(- or _)
            _time = p2.group()
        elif p3: #YYYYMMDD
            _time = p3.group()
        else:
            return UNKNOWN

        temp = _time.replace("_", "")
        temp2 = temp.replace("-", "")
        rtrDate = str(parse(temp2))

        return rtrDate

    def insert_dir_info(self, dir_id, device_id, dir_info, dir_name, dir_path, is_deleted):
        query = 'INSERT INTO directory_info VALUES({0:d},{1:d},"{2:s}","{3:s}","{4:s}",{5})' \
            .format(dir_id, device_id, dir_info, dir_name, dir_path, is_deleted)
        self._cursor.execute(query)
        self._connection.commit()

    def insert_file_info(self, file_id, dir_id, file_name, file_type, is_deleted, is_recover, is_rawdata, rawdata, file_path):
        query = 'INSERT INTO file_info VALUES({0:d},{1:d},"{2:s}",{3:d},{4},{5},{6},{7},"{8:s}")'\
            .format(file_id, dir_id, file_name, file_type, is_deleted, is_recover, is_rawdata, rawdata, file_path)
        self._cursor.execute(query)
        self._connection.commit()

    def insert_metdata(self, file_id, data_source, data_type, std_time, data2_value_text, data3_value_blob):
        self._metadata_idx += 1
        query = 'INSERT INTO metadata VALUES({0:d},{1:d},{2:d},{3:d},"{4:s}","{5:s}",{6})' \
                .format(self._metadata_idx, file_id, data_source, data_type, std_time, data2_value_text, data3_value_blob)
        self._cursor.execute(query)
        self._connection.commit()

    def insert_time_value(self, file_id, data_source, data_type, time_value, utc_time):
        self._filename_idx += 1
        query = 'INSERT INTO time_value VALUES({0:d},{1:d},{2:d},{3:d},"{4:s}",{5:d})'\
            .format(self._filename_idx, file_id, data_source, data_type, time_value, utc_time)
        self._cursor.execute(query)
        self._connection.commit()

    def get_recordmode_from_string(self, mode, data):
        event_set = ('motion', 'mot', 'motionmovie', 'p', 'pak', 'par', 'Park', 'parking', 'pmot', 'pmr')
        manual_set = ('camcoder', 'capture', 'dcim', 'man', 'manual', 'photo', 'user')
        normal_set = ('driving', 'blackbox', 'rec', 'normal', 'inf', 'n', 'i', 'alwa', 'alwaysmovie', 'cont', 'n-video')
        parking_set = ('driving shock', 'driving shock', 'e', 'event', 'evt', 'normal_to_event', 'parkingevent', 'pevt', 'p-video')
        temp = os.path.splitext(data)[0][0:]
        if mode == 'FILE':
            test = str(temp).lower().split('_')
        else:
            test = str(temp).lower().split('/')

        for item in test:
            if item in event_set:
                return (EVENT, item)
            elif item in manual_set:
                return (MANUAL, item)
            elif item in normal_set:
                return (NORMAL, item)
            elif item in parking_set:
                return (PARKING, item)

        return UNKNOWN #unknown

    def plaso_time_value(self, data):
        if data == 'M...':
            data_type = TIME_MODIFIED;
        elif data == '.A..':
            data_type = DATE_ACCESSED;
        elif data == '...B':
            data_type = TIME_CREATED;
        else:
            data_type = 0
        return data_type

    def device_channel(self, data):
        front_set = ('s','f', '1')
        rear_set = ('r', '2')
        dual_set = ('d')
        temp = os.path.splitext(data)[0][0:]
        test = str(temp).lower().split('_')
        for item in test:
            if item in front_set:
                return 'FRONT'
            elif item in rear_set:
                return 'REAR'
            elif item in dual_set:
                return 'DUAL'

        return UNKNOWN

    def database_close(self):
        self._cursor.close()
        self._connection.close()
        self._cursor = None
        self._connection = None

#클래스 네이밍 : input - output 명시해줌녀 좋음

class psort_database(DashcamMetadataDatabase):
    def __init__(self):
        self._connection = None
        self._cursor = None
        self._filename = None

    def get_default_info(self):
        print('no')
        #Get Directory
        #Get File

    def get_dir_info_query(self):
        query = 'SELECT inode, filename, MACB, description, extra FROM log2timeline'\
                'WHERE format = \'filestat\' and description like \'%type: directory%\''

    def get_file_info_query(self):
        query = 'SELECT inode, filename, MACB, description, extra, datetime FROM log2timeline '\
                'WHERE format = "filestat" and description like "%type: file%"'
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def get_query(self, where):
        query = 'SELECT inode, filename, MACB, description, extra, datetime FROM log2timeline {0:s}'.format(where)
        self._cursor.execute(query)
        return self._cursor.fetchall()


def main():
    parser = argparse.ArgumentParser(prog=' Dashcam-FIID (Filtering, Interpretation, Integration, Database)')
    parser.add_argument('--input_psort', type=str, help='input path of plaso result database as sqlite(4n6timeline')
    parser.add_argument('--output_result', type=str, help='input path of Integrated Analysis Result Database')

    args = parser.parse_args()

    """ Connect Psort Database"""
    input_psort = args.input_psort
    output_result = args.output_result

    if os.path.isfile(output_result):
        os.remove(output_result)

    """ CREATE IAR(Integrated Analysis Result) Database """
    iarDB = DashcamMetadataDatabase()
    iarDB.set_filename(output_result)
    iarDB.database_open()
    iarDB.initialize_database_file()
    iarDB.insert_default_data()

    """ OPEN PSORT Database """
    psDB = psort_database()
    psDB.set_filename(input_psort)
    psDB.database_open()

    device = _DEVICE_INFO()
    device.manufacture = 'Thinkware';   device.model = 'QXD3000';    device.version = '1.0';    device.filesystem = 'FAT32';    device.cam_channel = 2;
    device.container_format = 1;    device.location_type = 1;    device.filenameing_rule = 'Unknown';    device.timezone = 'UTC+9';    device.language = 'KR';

    iarDB.set_device_info(device)
    iarDB.work_filesystem(psDB.get_file_info_query()) # METADATA_SOURCE : FILE_NAME and TIMESTAMP IN FILESYSTEM
    iarDB.work_multimedia(psDB.get_query("WHERE description like '%list_of_chunks%'")) # METADATA_SOURCE : LIST_OF_CHUNKS IN MULTIMEDIA
    iarDB.work_metachunks(psDB.get_query("WHERE description like '%meta_chunks%'")) # METADATA_SOURCE : META_CHUNKS IN MULTIMEDIA
    iarDB.work_subtitle(psDB.get_query("WHERE description like '%subtitle_stream : %'"))
    iarDB.work_other_filies(VIDEO_STREAM, psDB.get_query("WHERE description like '%SEI NAL : %'"))
    iarDB.work_other_filies(NMEA, psDB.get_query("WHERE description like '%NMEA : %'"))
    iarDB.work_other_filies(CUSTOM_BINARY, psDB.get_query("WHERE description like '%custom_binary : %'"))

if __name__ == "__main__":
    main()
