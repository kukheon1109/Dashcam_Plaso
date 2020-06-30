# -*- coding: utf-8 -*-
"""Parser for multimedia file(like mp4, avi)"""
from __future__ import unicode_literals
from dfdatetime import java_time as dfdatetime_java_time

# -*- coding: utf-8 -*-
import os
import struct
import json

from plaso.lib import specification
from plaso.parsers import interface, dtfabric_parser
from plaso.parsers import manager

from plaso.parsers.AVI import pyavi #AVI Container
from plaso.parsers.MP4 import iso #MP4 Container

from plaso.containers import events
from plaso.containers import time_events

from dfvfs.helpers import text_file as dfvfs_text_file

from dfdatetime import time_elements as dftime_elements_time
from dfdatetime import posix_time
from plaso.lib import definitions

import pdb

class EventMetaData(events.EventData):
    "Metadata driven"
    DATA_TYPE =  'dashcam:metadata'

    def __init__(self):
        super(EventMetaData, self).__init__(data_type=self.DATA_TYPE)
        self.data_flag = None
        self.original_data = None


class MultimediaParser(interface.FileObjectParser):
    _INITIAL_FILE_OFFSET = None

    NAME = 'dashcam_metadata'
    DESCRIPTION = 'Parser for DashCam Multimeda files.'

    _plugin_classes = {}

    def __init__(self):
        super(MultimediaParser, self).__init__()
        self._meta_data = {}


    """ Step1. Signature check """
    @classmethod
    def GetFormatSpecification(cls):
        format_specification = specification.FormatSpecification(cls.NAME)

        # Parser for AVI file
        format_specification.AddNewSignature(  # AVI RIFF(0x52494646)
            b'\x52\x49\x46\x46', offset=0
        )

        # Parser for MP4 file
        format_specification.AddNewSignature(  # MP4 box(File Type Box)
            b'\x00\x00\x00\x20\x66\x74\x79\x70', offset=0
        )

        # Parser for custom binary
        format_specification.AddNewSignature(  # dat file
            b'\x53\x45\x4E\x53', offset=0
        )
        format_specification.AddNewSignature( # NMEA file
            b'\x24\x47', offset=0
        )

        return format_specification


    def event_generator(self, parser_mediator, parse_data, flag=''):
        event_data = EventMetaData()
        event_data.data_flag = flag
        event_data.original_data = parse_data
        date_time = dfdatetime_java_time.JavaTime(timestamp=0)
        event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_NOT_A_TIME)
        parser_mediator.ProduceEventWithEventData(event, event_data)

    def event_generator_element_time(self, parser_mediator, time_data, parse_data, flag=''):
        event_data = EventMetaData()
        event_data.data_flag = flag
        event_data.original_data = parse_data
        date_time = dftime_elements_time.TimeElements(time_elements_tuple=time_data)
        event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_RECORDED)
        parser_mediator.ProduceEventWithEventData(event, event_data)

    def event_generator_posix_time(self, parser_mediator, time_data, parse_data, flag=''):
        event_data = EventMetaData()
        event_data.data_flag = flag
        event_data.original_data = parse_data
        event = time_events.DateTimeValuesEvent(
            posix_time.PosixTime(timestamp=time_data), definitions.TIME_DESCRIPTION_RECORDED)
        parser_mediator.ProduceEventWithEventData(event, event_data)

    """ Step2. MULTIMEDIA FILE PARSING """
    def ParseFileObject(self, parser_mediator, file_object):

        file_object.seek(0, os.SEEK_SET)
        container_signature = file_object.read(8)
        if b'RIFF' in container_signature:  # AVI
            self.parseRIFF_AVI(parser_mediator, file_object)
        elif b'ftyp' in container_signature:  # MP4
            self.parseBMFF_MP4(parser_mediator, file_object)
        elif container_signature.startswith(b'SENS'):  # .dat - custom binary
            self.parseSENS_custom(parser_mediator, file_object)
        elif container_signature.startswith(b'$G'): # .NMEA file
            self.parseNMEA_file(parser_mediator, file_object)
        else:
            print('other files')

    """ PARSER FOR AVI """
    def parseRIFF_AVI(self, parser_mediator, file_object):
        temp_data = pyavi.file()
        temp_data.open_file_object(file_object)
        container_data = temp_data.get_riff_list()

        chunk_list = temp_data.get_chunkoflist() # List of Chunks - C
        self.event_generator(parser_mediator, chunk_list, 'list_of_chunks')

        for item in container_data.subchunks:
            if item.name == b'LIST':
                #print(item.name, item.chunktype)
                if item.chunktype == b'hdrl': # Meta Chunks - D / T / U
                    for item2 in item.subchunks:
                        #print(item2.name)
                        if item2.name == b'avih':
                            self.event_generator(parser_mediator, str(item2.data_dict), 'meta_chunks')
                        elif item2.name == b'LIST':
                            if item2.chunktype == b'strl':
                                for item3 in item2.subchunks:
                                    #print(item3.name)
                                    if item3.name == b'strh':
                                        self.event_generator(parser_mediator, str(item3.data_dict), 'meta_chunks')
                elif item.chunktype == b'INFO':
                    input_dict = {}
                    for item2 in item.subchunks:
                        if not item2.raw_data == None:
                            input_dict[item2.name.decode('utf-8')] = item2.raw_data.decode('utf-8')
                    if len(input_dict) > 0:
                        self.event_generator(parser_mediator, str(input_dict), 'meta_chunks')

                elif item.chunktype == b'movi':
                    for item2 in item.subchunks:
                        # subtitle stream
                        if (b'tx' or b'st' or b'sb') in item2.name: # Subtitle Stream - L / S / T
                            self.event_generator(parser_mediator, item2.raw_data, 'subtitle_stream')
                        # video stream
                        if b'dc' in item2.name:
                            rtr = self.parseSEI(parser_mediator, item2.raw_data)


    def parseSEI(self,parser_mediator, data):
        byte_scan = 0
        read_nal_cnt = 6
        size = len(data)
        while byte_scan < size:
            chk_nal = data[byte_scan:5]
            if b'\x00\x00\x00\x01\x06' in chk_nal:
                year = data[31:35].decode('utf-8') # 4
                month = data[35:37].decode('utf-8') # 2
                day = data[37:39].decode('utf-8') # 2e
                hour = data[39:41].decode('utf-8') # 2
                minute = data[41:43].decode('utf-8') #2
                second = data[43:45].decode('utf-8') #2
                latitude = struct.unpack('d', data[47:55])
                longtitude = struct.unpack('d', data[55:63])
                speed = struct.unpack('d', data[63:71])
                time_data = (int(year), int(month), int(day), int(hour), int(minute), int(second))
                speed_data = 'SPEED, ' + str(speed[0])
                gps_data = 'LOCATION, ' + str(latitude[0]) + ', ' + str(longtitude[0])
                self.event_generator_element_time(parser_mediator, time_data, speed_data, 'SEI NAL')
                self.event_generator_element_time(parser_mediator, time_data, gps_data, 'SEI NAL')
                return 'FOUND'
            else:
                return 'UNKNOWN'


    """ PARSER FOR MP4 """
    def parseBMFF_MP4(self, parser_mediator, file_object):

        container_data = iso.Mp4File(file_object)
        chunk_list = iso.chunk_of_list
        self.event_generator(parser_mediator, chunk_list, 'list_of_chunks') # List of Chunks - C
        # ToDo - trak(gmhd-text), udat box
        proprietary_meta = False
        proprietary_stsz = list()
        proprietary_stco = list()
        mdat_offset = 0
        mdat_data = None
        # MP4 container saved data in gmhd(trak), so get stsz and stco from trak, and get data
        for box in container_data.child_boxes:
            #if box.type == 'mdat':
                #mdat_offset = box.start_of_box
                #mdat_data = box.byte_string
            if box.type == 'moov':
                for box2 in box.child_boxes:
                    if box2.type == 'mvhd':
                        self.event_generator(parser_mediator, str(box2.box_info), 'meta_chunks') # Meta Chunks - D / T / U
                    elif box2.type == 'trak':
                        for box3 in box2.child_boxes:
                            if box3.type == 'tkhd':
                                self.event_generator(parser_mediator, str(box3.box_info), 'meta_chunks')  # Meta Chunks - D / T / U
                            elif box3.type == 'mdia':
                                for box4 in box3.child_boxes:
                                    if box4.type == 'mdhd':
                                        self.event_generator(parser_mediator, str(box4.box_info), 'meta_chunks')  # Meta Chunks - D / T / U
                                    elif box4.type == 'minf':
                                        for box5 in box4.child_boxes:
                                            if box5.type == 'gmhd': # for subtitle stream offset
                                                proprietary_meta = True
                                            if proprietary_meta and box5.type == 'stbl':
                                                for box6 in box5.child_boxes:
                                                    if box6.type == 'stco':
                                                        proprietary_stco = box6.box_info['entry_list']
                                                    if box6.type == 'stsz':
                                                        proprietary_stsz = box6.box_info['entry_list']
        if proprietary_meta: # Subtitle Stream - L / S / T
            print('GET MDAT DATA')
            cnt = 0
            for st_offset in proprietary_stco:
                file_object.seek(st_offset + 2, os.SEEK_SET)
                self.event_generator(parser_mediator, file_object.read(proprietary_stsz[cnt]), 'subtitle_stream')
                cnt = cnt + 1


    """ PARSER FOR DAT """
    def parseSENS_custom(self, parser_mediator, file_object):
        byte_scan = 0
        gps_bool = False
        size = file_object.get_size()

        while (byte_scan < size):
            chk_sig = file_object.read(8)
            if b'GPSI' in chk_sig:
                gps_bool = True
            elif b'setup' in chk_sig: # Device info(later)
                break
            elif gps_bool is False:
                file_object.seek(-8, os.SEEK_CUR)
            else:
                file_object.seek(-8, os.SEEK_CUR)

            if gps_bool:
                _time = struct.unpack('i', file_object.read(4))
                _onroad = struct.unpack('i', file_object.read(4))
                _latitude = struct.unpack('i', file_object.read(4))
                _longtitude = struct.unpack('i', file_object.read(4))
                _altitude = struct.unpack('i', file_object.read(4))
                #gps_data = 'LOCATION, ' + str(_time[0]) + str(_onroad[0]) + str(_latitude[0]) + str(_longtitude[0]) + str(_altitude[0])
                gps_data = 'LOCATION, ' + str(_latitude[0]) + ', ' + str(_longtitude[0]) + ', ' + str(_altitude[0])
                self.event_generator_posix_time(parser_mediator, _time[0],  gps_data, 'custom_binary')
            else:
                _time = struct.unpack('i', file_object.read(4))
                _z_value = struct.unpack('i', file_object.read(4))
                _y_value = struct.unpack('i', file_object.read(4))
                _x_value = struct.unpack('i', file_object.read(4))
                _speed = struct.unpack('i', file_object.read(4))
                #sensor_data = 'g-sensor , ' 'Z:' + str(_z_value) + 'Y:' + str(_y_value) + 'X:'+str(_x_value) + ' speed:' +str(_speed)
                sensor_data = '$GSENSOR, ' + str(_x_value[0]) + ', ' + str(_y_value[0]) + ', ' + str(_z_value[0])
                speed_data = 'SPEED, ' + str(_speed[0])
                self.event_generator_posix_time(parser_mediator, _time[0], sensor_data, 'custom_binary')
                self.event_generator_posix_time(parser_mediator, _time[0], speed_data, 'custom_binary')

            byte_scan = byte_scan + 20

    """ PARSER FOR NMEA """
    def parseNMEA_file(self, parser_mediator, file_object):
        text_file_object = dfvfs_text_file.TextFile(file_object, encoding='utf-8')

        for line in text_file_object.readlines():
            if 'GPRMC' in line:  # NMEA - L / S / T
                original = line
                split_data = original.split(',')

                hours = int(split_data[1][0:2])
                minutes = int(split_data[1][2:4])
                seconds = float(split_data[1][4:])
                day = int(split_data[9][0:2])
                month = int(split_data[9][2:4])
                year = 2000 + int(split_data[9][4:6])
                time_data = (year, month, day, hours, minutes, seconds)

                self.event_generator_element_time(parser_mediator, time_data, line, 'NMEA')
            elif 'GSENSOR' in line: # NMEA - L / S / T
                self.event_generator(parser_mediator, line, 'NMEA')


manager.ParsersManager.RegisterParser(MultimediaParser) # 파서 클래스 등

