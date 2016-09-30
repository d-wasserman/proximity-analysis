# --------------------------------
# Name: ChainedScoring.py
# Purpose: This tool will add scoring fields for every field past based on a threshold, and two return values.
# Current Owner: David Wasserman
# Last Modified: 09/18/2016
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

# Define input parameters
input_features = arcpy.GetParameterAsText(0)
score_fields = arcpy.GetParameterAsText(1)
threshold = arcpy.GetParameter(2)
if_less_than_score = arcpy.GetParameter(3)
if_more_than_score = arcpy.GetParameter(4)


# Function Definitions

def funcReport(function=None, reportBool=False):
    """This decorator function is designed to be used as a wrapper with other functions to enable basic try and except
     reporting (if function fails it will report the name of the function that failed and its arguments. If a report
      boolean is true the function will report inputs and outputs of a function.-David Wasserman"""

    def funcReport_Decorator(function):
        def funcWrapper(*args, **kwargs):
            try:
                funcResult = function(*args, **kwargs)
                if reportBool:
                    print("Function:{0}".format(str(function.__name__)))
                    print("     Input(s):{0}".format(str(args)))
                    print("     Ouput(s):{0}".format(str(funcResult)))
                return funcResult
            except Exception as e:
                print(
                    "{0} - function failed -|- Function arguments were:{1}.".format(str(function.__name__), str(args)))
                print(e.args[0])

        return funcWrapper

    if not function:  # User passed in a bool argument
        def waiting_for_function(function):
            return funcReport_Decorator(function)

        return waiting_for_function
    else:
        return funcReport_Decorator(function)


def arcToolReport(function=None, arcToolMessageBool=False, arcProgressorBool=False):
    """This decorator function is designed to be used as a wrapper with other GIS functions to enable basic try and except
     reporting (if function fails it will report the name of the function that failed and its arguments. If a report
      boolean is true the function will report inputs and outputs of a function.-David Wasserman"""

    def arcToolReport_Decorator(function):
        def funcWrapper(*args, **kwargs):
            try:
                funcResult = function(*args, **kwargs)
                if arcToolMessageBool:
                    arcpy.AddMessage("Function:{0}".format(str(function.__name__)))
                    arcpy.AddMessage("     Input(s):{0}".format(str(args)))
                    arcpy.AddMessage("     Ouput(s):{0}".format(str(funcResult)))
                if arcProgressorBool:
                    arcpy.SetProgressorLabel("Function:{0}".format(str(function.__name__)))
                    arcpy.SetProgressorLabel("     Input(s):{0}".format(str(args)))
                    arcpy.SetProgressorLabel("     Ouput(s):{0}".format(str(funcResult)))
                return funcResult
            except Exception as e:
                arcpy.AddMessage(
                        "{0} - function failed -|- Function arguments were:{1}.".format(str(function.__name__),
                                                                                        str(args)))
                print(
                    "{0} - function failed -|- Function arguments were:{1}.".format(str(function.__name__), str(args)))
                print(e.args[0])

        return funcWrapper

    if not function:  # User passed in a bool argument
        def waiting_for_function(function):
            return arcToolReport_Decorator(function)

        return waiting_for_function
    else:
        return arcToolReport_Decorator(function)


@arcToolReport
def arcPrint(string, progressor_Bool=False):
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


@arcToolReport
def FieldExist(featureclass, fieldname):
    """ArcFunction
     Check if a field in a feature class field exists and return true it does, false if not.- David Wasserman"""
    fieldList = arcpy.ListFields(featureclass, fieldname)
    fieldCount = len(fieldList)
    if (fieldCount >= 1):  # If there is one or more of this field return true
        return True
    else:
        return False


@arcToolReport
def AddNewField(in_table, field_name, field_type, field_precision="#", field_scale="#", field_length="#",
                field_alias="#", field_is_nullable="#", field_is_required="#", field_domain="#"):
    """ArcFunction
    Add a new field if it currently does not exist. Add field alone is slower than checking first.- David Wasserman"""
    if FieldExist(in_table, field_name):
        print(field_name + " Exists")
        arcpy.AddMessage(field_name + " Exists")
    else:
        print("Adding " + field_name)
        arcpy.AddMessage("Adding " + field_name)
        arcpy.AddField_management(in_table, field_name, field_type, field_precision, field_scale,
                                  field_length,
                                  field_alias,
                                  field_is_nullable, field_is_required, field_domain)
@arcToolReport
def score_value(value,threshold,if_less_score=1,if_more_score=0):
    """This function is intended to take a value (proximity for example), and check if it is <= a threshold,
    and return a score for if it is less than or more than based on the passed parameters. Defaults to binary (0,1)"""
    if value<=threshold:
        return if_less_score
    else:
        return if_more_score

# Main Function
def ChainedScore(in_fc, scoring_fields, threshold=0, if_less_score=1, if_more_score=0):
    """This tool will score fields based a theshold, and return values to those fields based on if it is less than
    or more than the threshold. All fields treated the same. """
    try:
        arcpy.env.overwriteOutput = True
        desc_in_fc = arcpy.Describe(in_fc)
        workspace = desc_in_fc.catalogPath
        fields_list = str(scoring_fields).split(";")
        new_score_fields = [
            arcpy.ValidateFieldName("SCORE_{0}".format(str(i).replace("DIST_", "", 1).replace("ANGLE_", "", 1)),
                                    workspace) for i in fields_list]
        arcPrint("Adding and Computing Score Fields.",True)
        for new_score_pair in zip(fields_list,new_score_fields):
            field_to_score= new_score_pair[0]
            new_score=new_score_pair[1]
            AddNewField(in_fc,new_score,"DOUBLE",field_alias=new_score)
            arcPrint("Computing score for field {0}. Returning {1} if value <= {2}, and {3} otherwise.".format(
                    str(new_score),str(threshold),str(if_less_score),str(if_more_score)),True)
            try:
                with arcpy.da.UpdateCursor(in_fc,[field_to_score,new_score]) as cursor:
                    for row in cursor:
                        row[1]=score_value(row[0],threshold,if_less_score,if_more_score)
                        cursor.updateRow(row)
            except:
                arcPrint("Could not process field {0}".format(new_score))

    except Exception as e:
        arcPrint(str(e.args[0]))
        print(e.args[0])


# End do_analysis function

# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    ChainedScore(input_features, score_fields, threshold, if_less_than_score, if_more_than_score)
