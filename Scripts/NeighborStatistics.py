# --------------------------------
# Name: NeighborStats.py
# Purpose: Given a spatial weights matrix & an input layer that relates to it, this tool will compute focal
# neighborhood statistics based the spatial relationships embodied in the weights matrix.
# Current Owner: David Wasserman
# Last Modified: 11/08/2019
# Copyright:   (c) David Wasserman
# ArcGIS Version:   10.4.1
# ArcGIS Pro Version: 2.7
# Python Version:   2.7/3.6
# --------------------------------
# Copyright 2019 David J. Wasserman
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
import pandas as pd
import proximity_lib as pl
import numpy as np


def weighted_standard_deviation(series, weights):
    """Compute the weighted standard deviation of a distribution.
    :param - series - series or numpy array - a set of values to calculate a std stat on
    :param - weights -series or numpy array - a set of weights the same len as the series """
    w_mean = np.average(series, weights=weights)
    w_var = np.average((series - w_mean) ** 2, weights=weights)
    return np.sqrt(w_var)


# Main Function
def compute_neighborhood_stats(in_fc, neighbor_fields, spatial_weights_matrix, output_feature_class,
                               statistics_to_compute=["sum", "mean", "std"], use_weights=True
                               ):
    """Given an input feature class and a corresponding spatial weights matrix, this tool will compute
    neighborhood level stats based on the spatial relationships defined in the SWM file.
    @param - in_fc - feature class with fields to focalize on the neighborhood level
    @param - neighbor_fields - fields to summarize. Depending on stats chosen, the words "SUM","AVG", or "STD"
    will be prepended to the new name
    @param - spatial_weights_matrix - swm file that denotes spatial relationships
    @param - output feature class - output feature class chosen for the computed copy with new fields added
    @param - statistics_to_compute- statistics chosen to compute based on the spatial relationships - options are
    denoted by a list with lower case choices between "sum","mean","std"
    @use_weights - boolean indicating if weights are used in SWM
    """
    try:
        arcpy.env.overwriteOutput = True
        workspace = os.path.dirname(in_fc)
        ws = "in_memory"
        pl.arc_print("Converting SWM file to in_memory table...")
        swm_table = os.path.join(ws, "swm_table")
        arcpy.ConvertSpatialWeightsMatrixtoTable_stats(spatial_weights_matrix, swm_table)
        pl.arc_print("Converting table to dataframe...")
        swm_df = pl.arcgis_table_to_df(swm_table)
        swm_df_cols = swm_df.columns
        swm_df_join_field = str(swm_df_cols[0]).upper()  # First Column should be join field
        swm_df_nid = "NID"
        swm_df_weight = "WEIGHT"
        swm_df = swm_df.set_index(swm_df_nid)
        pl.arc_print("Copying output feature classes...")
        input_feature_fields = [str(i.name) for i in arcpy.ListFields(input_features)]
        upper_case_fields = [i.upper() for i in input_feature_fields]
        feature_class_join_field = input_feature_fields[upper_case_fields.index(swm_df_join_field)]
        fc_fields = [feature_class_join_field]
        fc_fields.extend(neighbor_fields)
        arcpy.CopyFeatures_management(input_features, output_feature_class)
        pl.arc_print("Combining spatial weights matrix & feature class fields...")
        fc_df = pl.arcgis_table_to_df(output_feature_class, fc_fields)
        fc_df = fc_df.set_index(feature_class_join_field)
        swm_df_w_data = pd.merge(swm_df, fc_df, how="left", left_index=True, right_index=True)
        valid_statistics = ["sum", "mean", "std"]
        statistics_to_compute = [i for i in statistics_to_compute if i in valid_statistics]
        if not use_weights:
            pl.arc_print("Computing non-weighted neighborhood statistics...")
            swm_df_grps = swm_df_w_data.groupby(swm_df_join_field)
            swm_df_stats = swm_df_grps[neighbor_fields].agg(statistics_to_compute)
            swm_df_stats.columns = ["_".join(x) for x in swm_df_stats.columns.ravel()]
        # work in progress - next commit.
        else:  # Use weights
            pl.arc_print("Computing weighted neighborhood statistics...")
            neighbor_fields.append(swm_df_weight)
            product_fields = []
            sum_stats, mean_stats, std_stats = None, None, None
            for field in neighbor_fields:
                product_field = "temp_prod_" + str(field)
                swm_df_w_data[product_field] = swm_df_w_data[field] * swm_df_w_data[swm_df_weight]
                product_fields.append(product_field)  # create weighted products
            swm_df_grps = swm_df_w_data.groupby(swm_df_join_field)
            if "sum" in statistics_to_compute:
                pl.arc_print("Computing weighted sum...")
                swm_df_stats = swm_df_grps[product_fields].agg("sum")
                sum_stats = swm_df_stats.copy()
                sum_stats.columns = ["w_sum_" + i for i in neighbor_fields]
            if "mean" in statistics_to_compute:
                pl.arc_print("Computing weighted mean...")
                swm_df_stats = swm_df_grps[product_fields].agg("sum")
                mean_stats = swm_df_stats.copy()
                weights_sum = swm_df_grps[swm_df_weight].agg("sum")
                mean_stats = mean_stats.divide(weights_sum, axis="index")
                mean_stats.columns = ["w_mean_" + i for i in neighbor_fields]
            if "std" in statistics_to_compute:
                pl.arc_print("Computing weighted standard deviation...")
                std_stats = None
                for field in neighbor_fields:
                    new_std_col = "w_std_" + str(field)
                    series = swm_df_grps[[field, swm_df_weight]].apply(
                        lambda x: weighted_standard_deviation(x[field], x[swm_df_weight]))
                    if std_stats is None:
                        std_stats = pd.DataFrame({new_std_col: series})
                    else:
                        std_stats[new_std_col] = series
            swm_df_stats = None
            for potential_statistic_df in [sum_stats, mean_stats, std_stats]:
                if potential_statistic_df is None:
                    pass
                elif swm_df_stats is None:
                    swm_df_stats = potential_statistic_df
                else:
                    swm_df_stats = pd.concat([swm_df_stats, potential_statistic_df], axis=1)
        df_join_index_field = "DFJNIndex"
        swm_df_stats[df_join_index_field] = swm_df_stats.index
        pl.arc_print("Exporting new percentile dataframe to structured numpy array.", True)
        finalStandardArray = swm_df_stats.to_records()
        pl.arc_print(
            "Joining new fields to feature class. The new fields are {0}".format(str(swm_df_stats.columns))
            , True)
        arcpy.da.ExtendTable(output_feature_class, feature_class_join_field, finalStandardArray, df_join_index_field,
                             append_only=False)
        pl.arc_print("Script Completed Successfully.", True)
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
    neighbor_fields = arcpy.GetParameterAsText(1).split(";")
    spatial_weights_matrix = arcpy.GetParameterAsText(2)
    output_feature_class = arcpy.GetParameterAsText(3)
    use_weights = bool(arcpy.GetParameterAsText(4))
    use_sum = "sum" if bool(arcpy.GetParameterAsText(5)) else None
    use_average = "mean" if bool(arcpy.GetParameterAsText(6)) else None
    use_std = "std" if bool(arcpy.GetParameterAsText(7)) else None
    statistics_to_compute = [i for i in [use_sum, use_average, use_std] if i is not None]
    compute_neighborhood_stats(input_features, neighbor_fields, spatial_weights_matrix, output_feature_class,
                               statistics_to_compute, use_weights)
