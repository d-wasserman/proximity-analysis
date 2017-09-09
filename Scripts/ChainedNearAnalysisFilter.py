# --------------------------------
# Name: ChainedNearAnalysisFilter.py
# Purpose: This tool will conduct a near analysis that will add a new field for every Near Feature created by a filter
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


# Function Definitions

def func_report(function=None, reportBool=False):
    """This decorator function is designed to be used as a wrapper with other functions to enable basic try and except
     reporting (if function fails it will report the name of the function that failed and its arguments. If a report
      boolean is true the function will report inputs and outputs of a function.-David Wasserman"""

    def func_report_decorator(function):
        def func_wrapper(*args, **kwargs):
            try:
                func_result = function(*args, **kwargs)
                if reportBool:
                    print("Function:{0}".format(str(function.__name__)))
                    print("     Input(s):{0}".format(str(args)))
                    print("     Ouput(s):{0}".format(str(func_result)))
                return func_result
            except Exception as e:
                print(
                    "{0} - function failed -|- Function arguments were:{1}.".format(str(function.__name__), str(args)))
                print(e.args[0])

        return func_wrapper

    if not function:  # User passed in a bool argument
        def waiting_for_function(function):
            return func_report_decorator(function)

        return waiting_for_function
    else:
        return func_report_decorator(function)


def arc_tool_report(function=None, arcToolMessageBool=False, arcProgressorBool=False):
    """This decorator function is designed to be used as a wrapper with other GIS functions to enable basic try and except
     reporting (if function fails it will report the name of the function that failed and its arguments. If a report
      boolean is true the function will report inputs and outputs of a function.-David Wasserman"""

    def arc_tool_report_decorator(function):
        def func_wrapper(*args, **kwargs):
            try:
                func_result = function(*args, **kwargs)
                if arcToolMessageBool:
                    arcpy.AddMessage("Function:{0}".format(str(function.__name__)))
                    arcpy.AddMessage("     Input(s):{0}".format(str(args)))
                    arcpy.AddMessage("     Ouput(s):{0}".format(str(func_result)))
                if arcProgressorBool:
                    arcpy.SetProgressorLabel("Function:{0}".format(str(function.__name__)))
                    arcpy.SetProgressorLabel("     Input(s):{0}".format(str(args)))
                    arcpy.SetProgressorLabel("     Ouput(s):{0}".format(str(func_result)))
                return func_result
            except Exception as e:
                arcpy.AddMessage(
                    "{0} - function failed -|- Function arguments were:{1}.".format(str(function.__name__),
                                                                                    str(args)))
                print(
                    "{0} - function failed -|- Function arguments were:{1}.".format(str(function.__name__), str(args)))
                print(e.args[0])

        return func_wrapper

    if not function:  # User passed in a bool argument
        def waiting_for_function(function):
            return arc_tool_report_decorator(function)

        return waiting_for_function
    else:
        return arc_tool_report_decorator(function)


@arc_tool_report
def arc_print(string, progressor_Bool=False):
    """ This function is used to simplify using arcpy reporting for tool creation,if progressor bool is true it will
    create a tool label."""
    casted_string = str(string)
    if progressor_Bool:
        arcpy.SetProgressorLabel(casted_string)
        arcpy.AddMessage(casted_string)
        print(casted_string)
    else:
        arcpy.AddMessage(casted_string)
        print(casted_string)


@arc_tool_report
def field_exist(featureclass, fieldname):
    """ArcFunction
     Check if a field in a feature class field exists and return true it does, false if not.- David Wasserman"""
    fieldList = arcpy.ListFields(featureclass, fieldname)
    fieldCount = len(fieldList)
    if (fieldCount >= 1) and fieldname.strip():  # If there is one or more of this field return true
        return True
    else:
        return False


@arc_tool_report
def add_new_field(in_table, field_name, field_type, field_precision="#", field_scale="#", field_length="#",
                  field_alias="#", field_is_nullable="#", field_is_required="#", field_domain="#"):
    """ArcFunction
    Add a new field if it currently does not exist. Add field alone is slower than checking first.- David Wasserman"""
    if field_exist(in_table, field_name):
        print(field_name + " Exists")
        arcpy.AddMessage(field_name + " Exists")
    else:
        print("Adding " + field_name)
        arcpy.AddMessage("Adding " + field_name)
        arcpy.AddField_management(in_table, field_name, field_type, field_precision, field_scale,
                                  field_length,
                                  field_alias,
                                  field_is_nullable, field_is_required, field_domain)


@arc_tool_report
def constructSQLEqualityQuery(fieldName, value, dataSource, equalityOperator="=", noneEqualityOperator="is"):
    """Creates a workspace sensitive equality query to be used in arcpy/SQL statements. If the value is a string,
    quotes will be used for the query, otherwise they will be removed. Python 2-3 try except catch.(BaseString not in 3)
    David Wasserman"""
    try:  # Python 2
        if isinstance(value, (basestring, str)):
            return "{0} {1} '{2}'".format(arcpy.AddFieldDelimiters(dataSource, fieldName), equalityOperator,
                                          str(value))
        if value is None:
            return "{0} {1} {2}".format(arcpy.AddFieldDelimiters(dataSource, fieldName), noneEqualityOperator,
                                        "NULL")
        else:
            return "{0} {1} {2}".format(arcpy.AddFieldDelimiters(dataSource, fieldName), equalityOperator,
                                        str(value))
    except:  # Python 3
        if isinstance(value, (str)):  # Unicode only
            return "{0} {1} '{2}'".format(arcpy.AddFieldDelimiters(dataSource, fieldName), equalityOperator,
                                          str(value))
        if value is None:
            return "{0} {1} {2}".format(arcpy.AddFieldDelimiters(dataSource, fieldName), noneEqualityOperator,
                                        "NULL")
        else:
            return "{0} {1} {2}".format(arcpy.AddFieldDelimiters(dataSource, fieldName), equalityOperator,
                                        str(value))


@arc_tool_report
def arc_unique_values(table, field, filter_falsy=False):
    """This function will return a list of unique values from a passed field. If the optional bool is true,
    this function will scrub out null/falsy values. """
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        if filter_falsy:
            return sorted({row[0] for row in cursor if row[0]})
        else:
            return sorted({row[0] for row in cursor})


# Main Function
def chained_near_analysis_filter(in_fc, near_feature, near_filter_field, search_radius=None, location=False,
                                 angle=False, fid=False, method="PLANAR"):
    """This tool will conduct a near analysis that will add a new field for every feature layer genereated as the result
    of a make feature layer querying every unique value of a chosen field in the near feature class.
    Consider a Near Table if you want more detailed proximity information and are comfortable
      with a higher number of records"""
    try:
        arcpy.env.overwriteOutput = True
        workspace = os.path.dirname(in_fc)
        near_feature_value_list = arc_unique_values(near_feature, near_filter_field, True)
        input_fc_name = os.path.split(in_fc)[1]
        near_desc = arcpy.Describe(near_feature)
        input_near_ws = near_desc.catalogPath
        NEARFID = "NEAR_FID"
        NEARDISTField = "NEAR_DIST"
        NEARXField = "NEAR_X"
        NEARYField = "NEAR_Y"
        NEARAngleField = "NEAR_ANGLE"
        for feature_value in near_feature_value_list:
            query = constructSQLEqualityQuery(near_filter_field, feature_value, input_near_ws)
            layer_name = "F_" + str(feature_value)
            arcpy.MakeFeatureLayer_management(near_feature, layer_name, query)
            feature_name = str(layer_name)
            arc_print("Conducting NEAR Analysis with input feature class ({0}) and near feature layer ({1}).".format(
                input_fc_name, feature_name))
            arcpy.Near_analysis(in_fc, feature_name, search_radius, location, angle, method)
            new_dist_field_name = "DIST_" + feature_name
            new_angle_field_name = "ANGLE_" + feature_name
            new_fid_field_name = "FID_" + feature_name
            new_x_field_name = "X_" + feature_name
            new_y_field_name = "Y_" + feature_name
            arc_print("Calculating Near Feature specific fields for {0}.".format(feature_name))
            if field_exist(in_fc, NEARDISTField):
                valid_dist_field_name = arcpy.ValidateFieldName(new_dist_field_name, workspace)
                add_new_field(in_fc, valid_dist_field_name, "DOUBLE", field_alias=new_dist_field_name)
                arcpy.CalculateField_management(in_fc, valid_dist_field_name, "!NEAR_DIST!", "PYTHON_9.3")
            if field_exist(in_fc, NEARXField):
                valid_x_field_name = arcpy.ValidateFieldName(new_x_field_name, workspace)
                add_new_field(in_fc, valid_x_field_name, "DOUBLE", field_alias=new_x_field_name)
                arcpy.CalculateField_management(in_fc, valid_x_field_name, "!NEAR_X!", "PYTHON_9.3")
            if field_exist(in_fc, NEARYField):
                valid_y_field_name = arcpy.ValidateFieldName(new_y_field_name, workspace)
                add_new_field(in_fc, valid_y_field_name, "DOUBLE", field_alias=new_y_field_name)
                arcpy.CalculateField_management(in_fc, valid_y_field_name, "!NEAR_Y!", "PYTHON_9.3")
            if field_exist(in_fc, NEARAngleField):
                valid_angle_field_name = arcpy.ValidateFieldName(new_angle_field_name, workspace)
                add_new_field(in_fc, valid_angle_field_name, "DOUBLE", field_alias=new_angle_field_name)
                arcpy.CalculateField_management(in_fc, valid_angle_field_name, "!NEAR_ANGLE!", "PYTHON_9.3")
            if field_exist(in_fc, NEARFID) and fid:
                valid_fid_field_name = arcpy.ValidateFieldName(new_fid_field_name, workspace)
                add_new_field(in_fc, valid_fid_field_name, "DOUBLE", field_alias=new_fid_field_name)
                arcpy.CalculateField_management(in_fc, valid_fid_field_name, "!NEAR_FID!", "PYTHON_9.3")    
        arc_print("Deleting NEAR Fields from last feature.")
        try:
            arcpy.DeleteField_management(in_fc, NEARDISTField)
            arcpy.DeleteField_management(in_fc, NEARXField)
            arcpy.DeleteField_management(in_fc, NEARYField)
            arcpy.DeleteField_management(in_fc, NEARAngleField)
            arcpy.DeleteField_management(in_fc, NEARFID)
        except:
            arc_print("Could not delete near fields. QAQC Outputs.")
            pass
    except Exception as e:
        arc_print(str(e.args[0]))
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
