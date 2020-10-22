# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/DataTime.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/SciDataTool/tree/master/SciDataTool/Methods//DataTime
"""

from os import linesep
from logging import getLogger
from ._check import set_array, check_var, raise_
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .DataND import DataND

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.DataTime.time_to_freq import time_to_freq
except ImportError as error:
    time_to_freq = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class DataTime(DataND):
    """Class for fields defined in time space"""

    VERSION = 1

    # cf Methods.DataTime.time_to_freq
    if isinstance(time_to_freq, ImportError):
        time_to_freq = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataTime method time_to_freq: " + str(time_to_freq)
                )
            )
        )
    else:
        time_to_freq = time_to_freq
    # save and copy methods are available in all object
    save = save
    copy = copy

    def __init__(self, axes=None, FTparameters=-1, values=None, symbol="", name="", unit="", symmetries=-1, normalizations=-1, init_dict = None, init_str = None):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for SciDataTool type, -1 will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with property names as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for SciDataTool Object"""

        if init_str is not None:  # Load from a file
            init_dict = load_init_dict(init_str)[1]
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "axes" in list(init_dict.keys()):
                axes = init_dict["axes"]
            if "FTparameters" in list(init_dict.keys()):
                FTparameters = init_dict["FTparameters"]
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
        # Set the properties (value check and convertion are done in setter)
        # Call DataND init
        super(DataTime, self).__init__(axes=axes, FTparameters=FTparameters, values=values, symbol=symbol, name=name, unit=unit, symmetries=symmetries, normalizations=normalizations)
        # The class is frozen (in DataND init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        DataTime_str = ""
        # Get the properties inherited from DataND
        DataTime_str += super(DataTime, self).__str__()
        return DataTime_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from DataND
        if not super(DataTime, self).__eq__(other):
            return False
        return True

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)
        """

        # Get the properties inherited from DataND
        DataTime_dict = super(DataTime, self).as_dict()
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        DataTime_dict["__class__"] = "DataTime"
        return DataTime_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""

        # Set to None the properties inherited from DataND
        super(DataTime, self)._set_None()
