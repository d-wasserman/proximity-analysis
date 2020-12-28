# --------------------------------
# Name: ChainedNearAnalysis.py
# Purpose: This tool will conduct a near analysis that will add a new field for every Near Feature input into the
# Input Features dataset.
# Current Owner: David Wasserman
# Last Modified: 09/08/2017
# Copyright:   (c) David Wasserman
# ArcGIS Version:   10.4.1
# ArcGIS Pro Version: 2.7
# Python Version:   2.7/3.6
# --------------------------------
# Copyright 2016 David J. Wasserman
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
# --------------------------------
# Import Modules
import os, sys, arcpy
import proximity_lib as pl


# Main Function
def chained_near_analysis(in_fc, near_features, search_radius=None, location=False, angle=False, fid=False,
                          method="PLANAR"):
    """This tool will conduct a near analysis that will add a new field for every Near Feature input into the
    Input Features dataset. Unlike Near, this tool will create a column wise set of Near fields for every
    Near Feature rather than using the closest of all the near features input into the tool. This results in
     many more fields, so use this only if you have a specific need to know proximity for every feature within
     the Input Feature class. Consider a Near Table if you want more detailed proximity information and are comfortable
      with a higher number of records"""
    try:
        arcpy.env.overwriteOutput = True
        workspace = os.path.dirname(in_fc)
        near_features_list = near_features
        input_fc_name = os.path.split(in_fc)[1]
        NEARFID = "NEAR_FID"
        NEARDISTField = "NEAR_DIST"
        NEARXField = "NEAR_X"
        NEARYField = "NEAR_Y"
        NEARAngleField = "NEAR_ANGLE"
        for feature in near_features_list:
            desc = arcpy.Describe(feature.strip("'"))
            feature_name = str(desc.name)
            pl.arc_print(
                "Conducting NEAR Analysis with input feature class ({0}) and near feature ({1}).".format(input_fc_name,
                                                                                                         feature_name))
            arcpy.Near_analysis(in_fc, feature, search_radius, location, angle, method)
            new_dist_field_name = "DIST_" + feature_name
            new_angle_field_name = "ANGLE_" + feature_name
            new_fid_field_name = "FID_" + feature_name
            new_x_field_name = "X_" + feature_name
            new_y_field_name = "Y_" + feature_name
            pl.arc_print("Calculating Near Feature specific fields for {0}.".format(feature_name))
            if pl.field_exist(in_fc, NEARDISTField):
                valid_dist_field_name = arcpy.ValidateFieldName(new_dist_field_name, workspace)
                pl.add_new_field(in_fc, valid_dist_field_name, "DOUBLE", field_alias=new_dist_field_name)
                arcpy.CalculateField_management(in_fc, valid_dist_field_name, "!NEAR_DIST!", "PYTHON_9.3")
            if pl.field_exist(in_fc, NEARXField):
                valid_x_field_name = arcpy.ValidateFieldName(new_x_field_name, workspace)
                pl.add_new_field(in_fc, valid_x_field_name, "DOUBLE", field_alias=new_x_field_name)
                arcpy.CalculateField_management(in_fc, valid_x_field_name, "!NEAR_X!", "PYTHON_9.3")
            if pl.field_exist(in_fc, NEARYField):
                valid_y_field_name = arcpy.ValidateFieldName(new_y_field_name, workspace)
                pl.add_new_field(in_fc, valid_y_field_name, "DOUBLE", field_alias=new_y_field_name)
                arcpy.CalculateField_management(in_fc, valid_y_field_name, "!NEAR_Y!", "PYTHON_9.3")
            if pl.field_exist(in_fc, NEARAngleField):
                valid_angle_field_name = arcpy.ValidateFieldName(new_angle_field_name, workspace)
                pl.add_new_field(in_fc, valid_angle_field_name, "DOUBLE", field_alias=new_angle_field_name)
                arcpy.CalculateField_management(in_fc, valid_angle_field_name, "!NEAR_ANGLE!", "PYTHON_9.3")
            if pl.field_exist(in_fc, NEARFID) and fid:
                valid_fid_field_name = arcpy.ValidateFieldName(new_fid_field_name, workspace)
                pl.add_new_field(in_fc, valid_fid_field_name, "DOUBLE", field_alias=new_fid_field_name)
                arcpy.CalculateField_management(in_fc, valid_fid_field_name, "!NEAR_FID!", "PYTHON_9.3")
        pl.arc_print("Deleting NEAR Fields from last feature.")
        try:
            arcpy.DeleteField_management(in_fc, NEARDISTField)
            arcpy.DeleteField_management(in_fc, NEARXField)
            arcpy.DeleteField_management(in_fc, NEARYField)
            arcpy.DeleteField_management(in_fc, NEARAngleField)
            arcpy.DeleteField_management(in_fc, NEARFID)
        except:
            pl.arc_print("Could not delete near fields. QAQC Outputs.")
            pass
    except Exception as e:
        pl.arc_print(str(e.args[0]))
        print(e.args[0])


# End do_analysis function

# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Define input parameters
    input_features = arcpy.GetParameterAsText(0)
    near_features = str(arcpy.GetParameterAsText(1)).split(";")
    search_radius = arcpy.GetParameter(2)
    location = arcpy.GetParameter(3)
    angle = arcpy.GetParameter(4)
    fid = arcpy.GetParameter(5)
    method = arcpy.GetParameterAsText(6)
    chained_near_analysis(input_features, near_features, search_radius, location, angle, fid, method)
