import chunk
import os

from plaso.parsers.AVI.avi_chunk import ListChunk, LeafChunk
from plaso.parsers.AVI import avi_util

""" PLASO """
def get_file_size(fileobject):
    fileobject.seek(0,os.SEEK_END) # move the cursor to the end of the file
    size = fileobject.tell()
    fileobject.seek(0,0)
    return size
"""
def search_list(file, limit):
    chunks = list()
    bytes_explored = 0

    while (bytes_explored<limit):
        explored_chunk = None
        try:
            current_chunk = chunk.Chunk(file, bigendian=False)
            current_chunk_name = current_chunk.getname()
            
            current_chunk_size = current_chunk.getsize()
            # if it's a LIST chunk call recurivelly this function
            if current_chunk_name == b'LIST':
                current_chunk_type = current_chunk.read(4)
                explored_chunk = ListChunk(current_chunk_name, current_chunk_size, current_chunk_type)
                subchunks = search_list(file, current_chunk_size - 4)
                explored_chunk.add_subchunks(subchunks)

            # if it's a basic chunk call the utils function to collect its fields ('parse_chunk_data')
            elif bytes_explored + current_chunk_size + 8 <= limit:
                explored_chunk = LeafChunk(current_chunk_name, current_chunk_size)
                if current_chunk_size > 0:
                    avi_util.parse_chunk_data(file, current_chunk_name.decode('utf-8'), current_chunk, explored_chunk, current_chunk_size)

            # to avoid the chunk to be inserted in the wrong LIST chunk
            else:
                file.seek(-8,1)

        except EOFError:
            print('eof')
            break#return

        if explored_chunk is not None:
            bytes_explored = bytes_explored + explored_chunk.get_size() + 8
            chunks.append(explored_chunk)
        else:
            break
    return chunks
"""

# classes
class file(object):
    def __init__(self):
        self.object = None
        self.target_file = None
        self.chunk_of_list = [] #chunk list

    def open_file_object(self, object, mode='rb'):
        self.target_file = object
        print('open complete')
        return ""

    def get_chunkoflist(self):
        return self.chunk_of_list

    def close(self):
        self.target_file.close()
        print('close complete')
        return ""

    def check_file_signature_file_object(self):
        """
        Check_file_signature(fileobject) > boolean

        Checks if a file has an Object AVI File Signature
        """
        self.target_file.seek(0, os.SEEK_SET)
        if self.target_file.read(4) == b'RIFF':
            return b'AVI'

        return None

    def get_riff_list(self):
        file_size = get_file_size(self.target_file)
        # xml root tag
        root = list()

        bytes_explored = 0
        while (bytes_explored < file_size):
            current_chunk = chunk.Chunk(self.target_file, bigendian=False)

            # get the RIFF  'AVI ' chunk of the file
            current_chunk_name = current_chunk.getname()
            current_chunk_size = current_chunk.getsize()
            #self.chunk_of_list = current_chunk_name.decode('ascii')
            self.chunk_of_list.append(current_chunk_name.decode('ascii'))

            if current_chunk_name == b'RIFF':
                current_chunk_type = current_chunk.read(4)
                self.chunk_of_list.append(current_chunk_type.decode('ascii'))
                riffchunk = ListChunk(current_chunk_name, current_chunk_size, current_chunk_type)
                # parse the chunk. This is a recurrent function over the list chunks in the file
                avi_chunks = self.search_list(self.target_file, current_chunk_size - 4)

                # add the collected chunks
                riffchunk.add_subchunks(avi_chunks)
                #Integrated DB 넣을거 생각해서 변환하기

            else:
                #print(current_chunk_name)
                raw = file.read(current_chunk_size)
                unknown = LeafChunk("unknown", len(raw))
                unknown.add_rawdata(raw)


            bytes_explored += current_chunk_size + 8

        return  riffchunk

    def search_list(self, file, limit):
        chunks = list()
        bytes_explored = 0

        while (bytes_explored < limit):
            explored_chunk = None
            try:
                current_chunk = chunk.Chunk(file, bigendian=False)
                current_chunk_name = current_chunk.getname()
                self.chunk_of_list.append(current_chunk_name.decode('ascii'))

                current_chunk_size = current_chunk.getsize()
                # if it's a LIST chunk call recurivelly this function
                if current_chunk_name == b'LIST':
                    current_chunk_type = current_chunk.read(4)
                    self.chunk_of_list.append(current_chunk_type.decode('ascii'))
                    explored_chunk = ListChunk(current_chunk_name, current_chunk_size, current_chunk_type)
                    subchunks = self.search_list(file, current_chunk_size - 4)
                    explored_chunk.add_subchunks(subchunks)

                # if it's a basic chunk call the utils function to collect its fields ('parse_chunk_data')
                elif bytes_explored + current_chunk_size + 8 <= limit:
                    explored_chunk = LeafChunk(current_chunk_name, current_chunk_size)
                    if current_chunk_size > 0:
                        avi_util.parse_chunk_data(file, current_chunk_name.decode('utf-8'), current_chunk,
                                                  explored_chunk, current_chunk_size)

                # to avoid the chunk to be inserted in the wrong LIST chunk
                else:
                    file.seek(-8, 1)

            except EOFError:
                print('eof')
                break  # return

            if explored_chunk is not None:
                bytes_explored = bytes_explored + explored_chunk.get_size() + 8
                chunks.append(explored_chunk)
            else:
                break
        return chunks














