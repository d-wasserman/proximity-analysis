# proximity-analysis

Python-based geoprocessing tools for ArcMap and ArcGIS Pro that assist with proximity analysis tasks. The tools use Near Analysis functionality and spatial weights matrices to compute Euclidean and network-based proximity metrics.

## Table of Contents

- [Installation](#installation)
- [Tools](#tools)
  - [Compute Neighborhood Statistics](#compute-neighborhood-statistics)
  - [Chained Near Analysis](#chained-near-analysis)
  - [Chained Near Query Filter](#chained-near-query-filter)
  - [Chained Scoring](#chained-scoring)
- [License](#license)

---

## Installation

1. Clone or download this repository.
2. Open ArcMap or ArcGIS Pro.
3. Add the toolbox file (`proximity-analysis.tbx` for ArcMap, `proximity-analysis-103.tbx` for ArcGIS Pro 3.x) to your project via **Add Toolbox**.
4. The scripts in `Scripts/` are referenced by the toolbox automatically — keep them in the same relative location.

---

## Tools

### Compute Neighborhood Statistics

Uses a spatial weights matrix (SWM) to compute neighborhood statistics (sum, mean, standard deviation) between polygons.

#### Parameters

| Parameter | Description | Data Type |
|-----------|-------------|-----------|
| Input_Feature_Class | Input feature class that relates to the input SWM file. Must contain the fields to compute neighborhood statistics on. | Feature Class |
| Fields_to_Focalize | The fields from the input feature class to compute neighborhood statistics on. | Multiple Value |
| Spatial_Weights_Matrix | The spatial weights matrix file (`.swm`). | SWM File |
| Output_Feature_Class | Output feature class location containing the focalized fields. | Feature Class |
| Use_Weights | Whether to use the weights embedded in the SWM. Default is `True`. | Boolean |
| Compute_Sum | Whether to compute the neighborhood sum based on the spatial weights matrix. | Boolean |
| Compute_Average | Whether to compute the neighborhood mean based on the spatial weights matrix. | Boolean |
| Compute_Standard_Deviation | Whether to compute the neighborhood standard deviation based on the spatial weights matrix. | Boolean |

---

### Chained Near Analysis

Runs a Near Analysis and adds a separate distance (and optionally angle/location/FID) field for every Near Feature class provided, rather than overwriting a single `NEAR_DIST` field.

Unlike the standard Near tool, which retains only the closest feature across all inputs, this tool produces a column for each Near Feature (`DIST_{FeatureClassName}`, `ANGLE_{FeatureClassName}`, etc.), so you can compare proximity to multiple feature classes simultaneously. Field names are validated and may be truncated by the RDBMS (e.g., shapefiles).

> **Note:** Use a Near Table instead if you need detailed proximity information and are comfortable working with a higher row count.

#### Parameters

| Parameter | Description | Data Type |
|-----------|-------------|-----------|
| Input_Features | Input features (point, polyline, polygon, or multipoint). New fields are added to this dataset. | Feature Class |
| Near_Features | One or more feature layers or feature classes to measure distance to. Each produces a `DIST_{Name}` field (and optionally `ANGLE_{Name}`, `X_{Name}`, `Y_{Name}`, `FID_{Name}`). | Multiple Value |
| Search_Radius *(optional)* | Maximum search distance. If omitted, all near features are considered. Use a linear unit (e.g., `1000 Meters`) when using the Geodesic method. | Linear Unit |
| Location *(optional)* | If `LOCATION`, writes the x- and y-coordinates of the closest point on the near feature to `X_{Name}` and `Y_{Name}` fields. Default: `NO_LOCATION`. | Boolean |
| Angle *(optional)* | If `ANGLE`, writes the near angle to an `ANGLE_{Name}` field. Planar: −180 to 180, 0 = east. Geodesic: −180 to 180, 0 = north. Default: `NO_ANGLE`. | Boolean |
| Transfer_FID *(optional)* | If `True`, copies the near feature's FID to a `FID_{Name}` field alongside the distance. | Boolean |
| Method *(optional)* | `PLANAR` (default) uses flat-earth distances. `GEODESIC` accounts for the curvature of the earth — recommended for data in geographic coordinate systems (e.g., WGS84, Web Mercator) or for analysis spanning large areas. | String |

---

### Chained Near Query Filter

Runs a Near Analysis for every unique value in a chosen field of a single Near Feature class, producing one distance column per unique value. Equivalent to manually creating a feature layer for each unique value and running Near Analysis on each.

#### Parameters

| Parameter | Description | Data Type |
|-----------|-------------|-----------|
| Input_Features | Input features (point, polyline, polygon, or multipoint). New fields are added to this dataset. | Feature Class |
| Near_Feature | A single feature class whose unique field values drive the analysis. Produces `DIST_{Value}` (and optionally `ANGLE_{Value}`) fields. | Feature Class |
| Near_Feature_Field | The field in Near_Feature whose unique values are used to generate the per-category near feature sets. | Field |
| Search_Radius *(optional)* | Maximum search distance. If omitted, all near features are considered. Use a linear unit (e.g., `1000 Meters`) when using the Geodesic method. | Linear Unit |
| Location *(optional)* | If `LOCATION`, writes the x- and y-coordinates of the closest point to `X_{Name}` and `Y_{Name}` fields. Default: `NO_LOCATION`. | Boolean |
| Angle *(optional)* | If `ANGLE`, writes the near angle to an `ANGLE_{Name}` field. Default: `NO_ANGLE`. | Boolean |
| Transfer_FID *(optional)* | If `True`, copies the near feature's FID to a `FID_{Name}` field alongside the distance. | Boolean |
| Method *(optional)* | `PLANAR` (default) or `GEODESIC`. See [Chained Near Analysis](#chained-near-analysis) for details. | String |

---

### Chained Scoring

Scores fields by comparing each value against a lower and upper threshold, assigning one score when the value falls within the range and another when it falls outside. Designed to work directly with the distance fields produced by Chained Near Analysis — it automatically strips the `DIST_` and `ANGLE_` prefixes when naming the output `SCORE_` fields.

#### Parameters

| Parameter | Description | Data Type |
|-----------|-------------|-----------|
| Input_Features | Input features (point, polyline, polygon, or multipoint). New `SCORE_` fields are added to this dataset. | Feature Class |
| Fields_to_Score | Fields to evaluate against the threshold. Output fields are named `SCORE_{FieldName}` (with `DIST_` / `ANGLE_` prefixes stripped). | Multiple Value |
| Score_Threshold_Upper | Upper bound of the "within threshold" range (exclusive). Values strictly below this and at or above the lower bound are considered within the threshold. | Double |
| Score_Threshold_Lower | Lower bound of the "within threshold" range (inclusive). Values at or above this and below the upper bound are considered within the threshold. | Double |
| Score_If_Within_Threshold | Score assigned when the field value falls within the threshold range. | Double |
| Score_If_Outside_Threshold | Score assigned when the field value falls outside the threshold range. | Double |

---

## License

Copyright 2016 David J. Wasserman

Licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). See [`LICENSE`](LICENSE) for details.
