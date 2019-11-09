# --------------------------------
# Name: ChainedScoring.py
# Purpose: This tool will add scoring fields for every field past based on a threshold, and two return values.
# Current Owner: David Wasserman
# Last Modified: 08/03/2017
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


@pl.arc_tool_report
def score_value(value, threshold_upper, threshold_lower=0, if_within_score=1, if_outside_score=0):
    """This function is intended to take a value (proximity for example), and check if it is <= a threshold,
    and return a score for if it is less than or more than based on the passed parameters. Defaults to binary (0,1)"""
    if value >= threshold_lower and value <= threshold_upper:
        return if_within_score
    else:
        return if_outside_score


# Main Function
def chained_scoring_func(in_fc, scoring_fields, threshold_upper, threshold_lower=0, if_less_score=1, if_more_score=0):
    """This tool will score fields based a  upper and lower bound threhsold, and return values to those fields based on if it is less than
    or more than the threshold. All fields treated the same. """
    try:
        arcpy.env.overwriteOutput = True
        desc_in_fc = arcpy.Describe(in_fc)
        workspace = desc_in_fc.catalogPath
        fields_list = scoring_fields
        new_score_fields = [
            arcpy.ValidateFieldName("SCORE_{0}".format(str(i).replace("DIST_", "", 1).replace("ANGLE_", "", 1)),
                                    workspace) for i in fields_list]
        pl.arc_print("Adding and Computing Score Fields.", True)
        for new_score_pair in zip(fields_list, new_score_fields):
            field_to_score = new_score_pair[0]
            new_score = new_score_pair[1]
            pl.add_new_field(in_fc, new_score, "DOUBLE", field_alias=new_score)
            pl.arc_print(
                "Computing score for field {0}. Returning {1} if value <= {2} and >= {3}, and {4} otherwise.".format(
                    str(new_score), str(if_less_score), str(threshold_upper), str(threshold_lower), str(if_more_score)),
                True)
            try:
                with arcpy.da.UpdateCursor(in_fc, [field_to_score, new_score]) as cursor:
                    for row in cursor:
                        row[1] = score_value(row[0], threshold_upper, threshold_lower, if_less_score, if_more_score)
                        cursor.updateRow(row)
            except:
                pl.arc_print("Could not process field {0}".format(new_score))

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
    score_fields = str(arcpy.GetParameterAsText(1)).split(";")
    threshold_upper = arcpy.GetParameter(2)
    threshold_lower = arcpy.GetParameter(3)
    if_within_score = arcpy.GetParameter(4)
    if_outside_score = arcpy.GetParameter(5)
    chained_scoring_func(input_features, score_fields, threshold_upper, threshold_lower, if_within_score,
                         if_outside_score)
