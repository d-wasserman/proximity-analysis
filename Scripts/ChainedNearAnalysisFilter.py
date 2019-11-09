# --------------------------------
# Name: ChainedNearAnalysisFilter.py
# Purpose: This tool will conduct a near analysis that will pl.add a new field for every Near Feature created by a filter
# using the Make Feature Layer tool on every unique attribute in a near features field.
# Current Owner: David Wasserman
# Last Modified: 09/08/2017
# Copyright:   (c) CoAdapt
# ArcGIS Version:   10.4.1
# Python Version:   2.7
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


# Function Definitions


# Main Function
def chained_near_analysis_filter(in_fc, near_feature, near_filter_field, search_radius=None, location=False,
                                 angle=False, fid=False, method="PLANAR"):
    """This tool will conduct a near analysis that will pl.add a new field for every feature layer genereated as the result
    of a make feature layer querying every unique value of a chosen field in the near feature class.
    Consider a Near Table if you want more detailed proximity information and are comfortable
      with a higher number of records"""
    try:
        arcpy.env.overwriteOutput = True
        workspace = os.path.dirname(in_fc)
        near_feature_value_list = pl.arc_unique_values(near_feature, near_filter_field, True)
        input_fc_name = os.path.split(in_fc)[1]
        near_desc = arcpy.Describe(near_feature)
        input_near_ws = near_desc.catalogPath
        NEARFID = "NEAR_FID"
        NEARDISTField = "NEAR_DIST"
        NEARXField = "NEAR_X"
        NEARYField = "NEAR_Y"
        NEARAngleField = "NEAR_ANGLE"
        for feature_value in near_feature_value_list:
            query = pl.constructSQLEqualityQuery(near_filter_field, feature_value, input_near_ws)
            layer_name = "F_" + str(feature_value)
            arcpy.MakeFeatureLayer_management(near_feature, layer_name, query)
            feature_name = str(layer_name)
            pl.arc_print("Conducting NEAR Analysis with input feature class ({0}) and near feature layer ({1}).".format(
                input_fc_name, feature_name))
            arcpy.Near_analysis(in_fc, feature_name, search_radius, location, angle, method)
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
    near_feature = str(arcpy.GetParameterAsText(1))
    near_filter_field = arcpy.GetParameterAsText(2)
    search_radius = arcpy.GetParameter(3)
    location = arcpy.GetParameter(4)
    angle = arcpy.GetParameter(5)
    fid = arcpy.GetParameter(6)
    method = arcpy.GetParameterAsText(7)
    chained_near_analysis_filter(input_features, near_feature, near_filter_field, search_radius, location, angle, fid,
                                 method)
