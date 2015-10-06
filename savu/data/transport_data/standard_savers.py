# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. module:: standard_loaders
   :platform: Unix
   :synopsis: Classes for different experimental setups containing standard
   data loaders.

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""
import h5py
import logging

from mpi4py import MPI
import numpy as np

NX_CLASS = 'NX_class'


class TomographySavers(object):
    """
    This class is called from a tomography loader when using a standard saver.
    It deals with saving of the data to different standard formats
    """

    def __init__(self, exp, params):
        self.saver_setup(exp)
        self.parameters = params

    def saver_setup(self, exp):
        pass

    def save_to_hdf5(self, exp):
        dtype = np.float32
        for key in exp.index["out_data"].keys():
            out_data = exp.index["out_data"][key]
            out_data.backing_file = self.create_backing_h5(key, exp.meta_data)
            out_data.group_name, out_data.group = \
                self.create_entries(out_data.backing_file, out_data,
                                    exp.meta_data, key, dtype)
            #self.output_meta_data(group, out_data, exp.meta_data, dtype)

    def create_backing_h5(self, key, expInfo):
        """
        Create a h5 backend for output data
        """
        filename = expInfo.get_meta_data(["filename", key])
        if expInfo.get_meta_data("mpi") is True:
            backing_file = h5py.File(filename, 'w', driver='mpio',
                                     comm=MPI.COMM_WORLD)
        else:
            backing_file = h5py.File(filename, 'w')

        print "creating file", filename
        if backing_file is None:
            raise IOError("Failed to open the hdf5 file")

        logging.debug("Creating file '%s' '%s'",
                      expInfo.get_meta_data("group_name"),
                      backing_file.filename)

        return backing_file

    def create_entries(self, backing_file, data, expInfo, key, dtype):
        group_name = expInfo.get_meta_data(["group_name", key])
        group = backing_file.create_group(group_name)
        group.attrs[NX_CLASS] = 'NXdata'
        group.attrs['signal'] = 'data'

        params = self.set_name("data")
        self.output_data_to_file(group, params, data.get_shape(), dtype)
        data.data = params["name"]
        return group_name, group
#
#    def output_meta_data(self, group, data, expInfo, dtype):
#        output_list = self.get_output_list(expInfo, data)
#
#        for name in output_list:
#            params = self.set_name(name)
#            value = expInfo.get_meta_data(name)
#            # just numpy arrays for now
#            if (type(value).__module__) in np.__name__:
#                self.output_data_to_file(group, params, value.shape, dtype)
#                params['name'][...] = value
#
#    def get_output_list(self, expInfo, data):
#        if self.parameters is False:
#            pattern = data.get_pattern_name()
#            if isinstance(data, ds.Raw):
#                pattern = "RAW"
#            return self.get_pattern_meta_data(data, pattern)
#        else:
#            meta_data = []
#            for key in expInfo.get_dictionary().keys():
#                meta_data.append(key)
#            return meta_data
#
#    # Temporary: Need to move this somewhere else?
#    def get_pattern_meta_data(self, pattern):
#        theDict = {}
#        theDict['RAW'] = ["image_key", "control", "rotation_angle"]
#        theDict['PROJECTION'] = ["rotation_angle"]
#        theDict['SINOGRAM'] = theDict['PROJECTION']
#
#        try:
#            return theDict['pattern']
#        except KeyError:
#            print "Warning: No meta_data output is associated with the \
#                                                            pattern:", pattern
#            return []

    def output_data_to_file(self, group, params, shape, dtype):
        group.attrs['signal'] = params['name']
        params['name'] = group.create_dataset(params['name'], shape, dtype)

    def set_name(self, name):
        params = {}
        params['name'] = name
        return params
