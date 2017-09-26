# ProximityAnalysis
ArcGIS (10.4.1) Scripting Tools developed to aid with proximity analysis. Tools listed below.  

# Chained Near (Analysis)
This tool will conduct a chained near analysis creating multiple near proximity fields for each near feature class given to it.
# Summary
This tool will conduct a near analysis that will add a new field for every Near Feature input into the Input Features dataset. Unlike Near, this tool will create a column wise set of Near fields for every Near Feature rather than using the closest of all the near features input into the tool. This results in many more fields, so use this only if you have a specific need to know proximity for every feature within the Input Feature class. Consider a Near Table if you want more detailed proximity information and are comfortable with a higher number of records.

# Parameters
<table width="100%" border="0" cellpadding="5">
<tbody>
<tr>
<th width="30%">
<b>Parameter</b>
</th>
<th width="50%">
<b>Explanation</b>
</th>
<th width="20%">
<b>Data Type</b>
</th>
</tr>
<tr>
<td class="info">Input_Features</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><P><SPAN>	</SPAN></P><P><SPAN>The input features that can be point, polyline, polygon, or multipoint type. Will have new fields added to it. </SPAN></P></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Feature Class</td>
</tr>
<tr>
<td class="info">Near_Features</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>One or more feature layers or feature classes containing near feature candidates. The near features can be of point, polyline, polygon, or multipoint. If mutliple features are chosen, each one will be given a separate field in the form of "DIST_{Feature Class Name}", or "ANGLE_{Feature Class Name}. Field names are validated so may be subject to truncation if the RDBMS requires it (shapefile). </SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Multiple Value</td>
</tr>
<tr>
<td class="info">Search_Radius (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>The radius used to search for near features. If no value is specified, all near features are considered. If a distance but no unit or unknown is specified, the units of the coordinate system of the input features are used. If the Geodesic option is used, a linear unit such as Kilometers or Miles should be used.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Linear unit</td>
</tr>
<tr>
<td class="info">Location (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Specifies whether x- and y-coordinates of the closest location of the near feature will be written to the X_{Feature Class Name} and Y_{Feature Class Name}  fields.</SPAN></P><P><SPAN>NO_LOCATION - Location information will not be written to the output table. This is the default.</SPAN></P><P><SPAN>LOCATION - Location information will be written to the output table.</SPAN></P><P><SPAN /></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Angle (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Specifies whether the near angle will be calculated and written to a ANGLE_{Feature Name} field in the output table. A near angle measures direction of the line connecting an input feature to its nearest feature at their closest locations. When the PLANAR method is used in the method parameter, the angle is within the range of -180 to 180, with 0 to the east, 90 to the north, 180 (or -180) to the west, and -90 to the south. When the GEODESIC method is used, the angle is within the range of -180 to 180, with 0 to the north, 90 to the east, 180 (or -180) to the south, and -90 to the west.</SPAN></P><P><SPAN>NO_ANGLE -The near angle values will not be written. This is the default.</SPAN></P><P><SPAN>ANGLE - The near angle values will be written to the ANGLE_{Feature Class Name}  field.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Transfer FID (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>If True, the FID of the Near Feature will be transferred to the input feature class along side the NEAR_Distance.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Method (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Determines whether to use a shortest path on a spheroid (geodesic) or a flat earth (planar) method. It is strongly suggested to use the Geodesic method with data stored in a coordinate system that is not appropriate for distance measurements (for example, Web Mercator or any geographic coordinate system) and any analysis that spans a large geographic area.</SPAN></P><P><SPAN>PLANAR -Uses planar distances between the features. This is the default.</SPAN></P><P><SPAN>GEODESIC -Uses geodesic distances between features. This method takes into account the curvature of the spheroid and correctly deals with data near the dateline and poles.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">String</td>
</tr>
</tbody>
</table>

# Chained Near Query Filter (Analysis)

This tool will conduct a chained near analysis creating multiple near proximity fields for each layer generated based on a chosen fields unique values by a Make Feature Layer query. 

# Summary

This tool will conduct a near analysis that will add a new field for every unique value found in the Near Feature
Filter Field relative to the Input Features dataset. Unlike Near, this tool will create multiple column wise near
fields for every unique set of field values within the Near Feature that is being compared to the Input Feature
class. This tool is the same as making a feature layer for every unique value in the Near Feature and then
running a Near Analysis tool on each of the output query layers. 

# Parameters
<table width="100%" border="0" cellpadding="5">
<tbody>
<tr>
<th width="30%">
<b>Parameter</b>
</th>
<th width="50%">
<b>Explanation</b>
</th>
<th width="20%">
<b>Data Type</b>
</th>
</tr>
<tr>
<td class="info">Input_Features</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><P><SPAN>	</SPAN></P><P><SPAN>The input features that can be point, polyline, polygon, or multipoint type. Will have new fields added to it. </SPAN></P></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Feature Class</td>
</tr>
<tr>
<td class="info">Near_Feature</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>One feature class that will have a field chosen to generate unique layers for comparison to the Input features. The near features can be of point, polyline, polygon, or multipoint. For each layer generated, each one will be given a separate field in the form of "DIST_{Feature Layer Name}", or "ANGLE_{Feature Layer Name}. Field names are validated so may be subject to truncation if the RDBMS requires it (shapefile). </SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Multiple Value</td>
</tr>
<tr>
<td class="info">Near_Feature_Field</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This is the field that is used to generate unique near feature sets that will be compared to the Input Feature class.  </SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Single Value</td>
</tr>
<tr>
<td class="info">Search_Radius (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>The radius used to search for near features. If no value is specified, all near features are considered. If a distance but no unit or unknown is specified, the units of the coordinate system of the input features are used. If the Geodesic option is used, a linear unit such as Kilometers or Miles should be used.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Linear unit</td>
</tr>
<tr>
<td class="info">Location (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Specifies whether x- and y-coordinates of the closest location of the near feature will be written to the X_{Feature Class Name} and Y_{Feature Class Name}  fields.</SPAN></P><P><SPAN>NO_LOCATION - Location information will not be written to the output table. This is the default.</SPAN></P><P><SPAN>LOCATION - Location information will be written to the output table.</SPAN></P><P><SPAN /></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Angle (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Specifies whether the near angle will be calculated and written to a ANGLE_{Feature Name} field in the output table. A near angle measures direction of the line connecting an input feature to its nearest feature at their closest locations. When the PLANAR method is used in the method parameter, the angle is within the range of -180 to 180, with 0 to the east, 90 to the north, 180 (or -180) to the west, and -90 to the south. When the GEODESIC method is used, the angle is within the range of -180 to 180, with 0 to the north, 90 to the east, 180 (or -180) to the south, and -90 to the west.</SPAN></P><P><SPAN>NO_ANGLE -The near angle values will not be written. This is the default.</SPAN></P><P><SPAN>ANGLE - The near angle values will be written to the ANGLE_{Feature Class Name}  field.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Transfer FID (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>If True, the FID of the Near Feature will be transferred to the input feature class along side the NEAR_Distance.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Method (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Determines whether to use a shortest path on a spheroid (geodesic) or a flat earth (planar) method. It is strongly suggested to use the Geodesic method with data stored in a coordinate system that is not appropriate for distance measurements (for example, Web Mercator or any geographic coordinate system) and any analysis that spans a large geographic area.</SPAN></P><P><SPAN>PLANAR -Uses planar distances between the features. This is the default.</SPAN></P><P><SPAN>GEODESIC -Uses geodesic distances between features. This method takes into account the curvature of the spheroid and correctly deals with data near the dateline and poles.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">String</td>
</tr>
</tbody>
</table>

# Chained Scoring (Analysis)
This tool score incoming features based on selected fields by checking if it is below a threshold for each field and then returning chosen values for if it is greater than or less than the threshold. 
# Summary
This tool will score every field selected by the tool, and return a value based on whether the value for that field (IE Proximity), is less than or equal to the set threshold. This tool is intended to be used with the Chained Near Analysis tool, and will even remove the "DIST_" or "ANGLE_" text elements of the new created field names when scoring proximity fields. 

# Parameters
<table width="100%" border="0" cellpadding="5">
<tbody>
<tr>
<th width="30%">
<b>Parameter</b>
</th>
<th width="50%">
<b>Explanation</b>
</th>
<th width="20%">
<b>Data Type</b>
</th>
</tr>
<tr>
<td class="info">Input_Features</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><DIV><P><SPAN /></P><P><SPAN>The input features that can be point, polyline, polygon, or multipoint type. Will have new fields added to it. </SPAN></P></DIV></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Feature Class</td>
</tr>
<tr>
<td class="info">Fields_to_Score</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><DIV><P><SPAN>These are the fields that will be compared against the threshold value chosen, and then will be used to generate new scoring fields based on the passed field names. </SPAN></P></DIV></DIV></DIV><div class="noContent" style="text-align:center; margin-top: -1em">___________________</div><br />
<span style="font-weight: bold">Python Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><DIV><P><SPAN><SPAN>new_score_fields</SPAN></SPAN><SPAN><SPAN /></SPAN><SPAN STYLE="font-weight:bold;"><SPAN>= </SPAN></SPAN><SPAN><SPAN>[</SPAN></SPAN><SPAN /><SPAN><SPAN>arcpy.ValidateFieldName(</SPAN></SPAN><SPAN><SPAN>"SCORE_{0}"</SPAN></SPAN><SPAN><SPAN>.format(</SPAN></SPAN><SPAN><SPAN>str</SPAN></SPAN><SPAN><SPAN>(i).replace(</SPAN></SPAN><SPAN><SPAN>"DIST_"</SPAN></SPAN><SPAN><SPAN>, </SPAN></SPAN><SPAN><SPAN>""</SPAN></SPAN><SPAN><SPAN>, </SPAN></SPAN><SPAN><SPAN>1</SPAN></SPAN><SPAN><SPAN>).replace(</SPAN></SPAN><SPAN><SPAN>"ANGLE_"</SPAN></SPAN><SPAN><SPAN>, </SPAN></SPAN><SPAN><SPAN>""</SPAN></SPAN><SPAN><SPAN>, </SPAN></SPAN><SPAN><SPAN>1</SPAN></SPAN><SPAN><SPAN>)),</SPAN></SPAN><SPAN /><SPAN><SPAN>workspace) </SPAN></SPAN><SPAN STYLE="font-weight:bold;"><SPAN>for </SPAN></SPAN><SPAN><SPAN>i </SPAN></SPAN><SPAN STYLE="font-weight:bold;"><SPAN>in </SPAN></SPAN><SPAN><SPAN>fields_list]</SPAN></SPAN></P><P><SPAN /></P></DIV></DIV></DIV></td>
<td class="info" align="left">Multiple Value</td>
</tr>
<tr>
<td class="info">Score_Threshold_Upper</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This represents the upper value of the near values that will be considered for scoring in a proximity analysis. If the value is greater than or equal to this value and below the upper threshold value, it is considered "Within" the threshold. </SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
<tr>
<td class="info">Score_Threshold_Lower</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This represents the lower value of the near values that will be considered for scoring in a proximity analysis. If the value is greater than or equal to this value and below the upper threshold value, it is considered "Within" the threshold</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
<tr>
<td class="info">Score_If_WithinThreshold</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This is the score the field will have if it is within the threshold value bounds.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
<tr>
<td class="info">Score_If_Outside_Threshold</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This is the score the field will have if it is outside the threshold value bounds.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
</tbody>
</table>

# Relative Proximity Reclassification (DataDrivenReclass)
This tool is designed to aid in the creation of data driven suitability layers. The tool takes a reference layer and a variable layer as inputs. The reference layer represents the features that you want to create suitabilities for ("Single Family Residential"), and the variable layer represents the variable that relates to the reference layer (Parks for Recreation).
# Summary
This tool is designed to aid in the creation of data driven suitability layers. The tool takes a reference layer and a variable layer as inputs. The reference layer represents the features that you want to create suitabilities for ("Single Family Residential"), and the variable layer represents the variable that relates to the reference layer (Parks for Recreation). Based on the average and standard deviation of the distance each object in the reference layer is from the variable layer, a euclidean distance away from the variable layer is reclassified by a remap table that reclassies the mean to be the top value with a reduction in suitability value for every quarter standard deviation. 

# Parameters
<table width="100%" border="0" cellpadding="5">
<tbody>
<tr>
<th width="30%">
<b>Parameter</b>
</th>
<th width="50%">
<b>Explanation</b>
</th>
<th width="20%">
<b>Data Type</b>
</th>
</tr>
<tr>
<td class="info">Reference_Layer</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><DIV><P><SPAN /></P><P><SPAN>This input is what you want a suitability of and serves as the "reference layer" that is used to create the statistics that drive the reclassification based on this layers proximity to the variable layer. For example, in the illustration single family residential parcels are used as this input. </SPAN></P></DIV></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Feature Class</td>
</tr>
<tr>
<td class="info">Variable_Layer</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This input is the variable that corresponds to the suitability layer, and from this input a Euclidean distance raster will be created and reclassified based on its proximity statistics from to the suitability layer. For example, in the illustration above retail parcels are used to create the output.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
<tr>
<td class="info">Reclassified_Suitability_Layer</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>This is the output destination for the reclassified suitability input raster. Example above shows the reclassified raster going from green to red. This might need to be reclassified again if the variable of interest is not an attractor variable (flpping it). Keep the name under 13 characters.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
<tr>
<td class="info">Invert_Raster</td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>If checked, the output raster will be inverted so that the max value of 9 is assigned to values further away from the reference layer.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Double</td>
</tr>
</tbody>
</table>