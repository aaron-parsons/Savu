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
.. module:: meta_data
   :platform: Unix
   :synopsis: Contains the MetaData class which holds all information required 
   by the pipeline throughout processing.  An instance of MetaData is held by
   the Experiment class.

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""
from savu.data.plugin_list import PluginList

class MetaData(object):
    """
    The MetaData class creates a dictionary of all meta data which can be 
    accessed using the get and set methods. It also holds an instance of 
    PluginList.
    """
   
    def __init__(self, options):
        self.dict = options
        self.load_experiment_collection()
        self.plugin_list = PluginList(self)


    def load_experiment_collection(self):
        transport_collection = self.dict["transport"] + "_experiment"                    
        class_name = ''.join(x.capitalize() for x in transport_collection.split('_'))
        self.add_base(globals()[class_name])
        
        
    def add_base(self, transport):
        cls = self.__class__
        self.__class__ = cls.__class__(cls.__name__, (cls, transport), {})
        

    def set_meta_data(self, name, value):
        self.dict[name] = value
    

    def get_meta_data(self, name):
        return self.dict[name]        
    
    
    def get_dictionary(self):
        return self.dict
        

class Hdf5Experiment():
    """
    The Hdf5Experiment class is inherited by Experiment class at 
    runtime and performs initial setup of metadata
    """    
    def set_transport_meta_data(self):
        
        # load dark, flat
        #self.set_meta_data("dark", dark)
        #self.set_meta_data("flat", flat)
        pass
    

class distArrayExperiment():
    """
    The Hdf5Experiment class is inherited by Experiment class at 
    runtime and performs initial setup of metadata
    """
    def set_transport_meta_data(self):    
        # load dark, flat, rotation angle?
        self.set_meta_data("dark", dark)
        self.set_meta_data("flat", flat)
