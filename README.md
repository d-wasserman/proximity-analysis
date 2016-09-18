# ProximityAnalysis
ArcGIS (10.4.1) Scripting Tools developed to aid with proximity analysis. Tools listed below.  

#Chained Near (Analysis)
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
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Specifies whether x- and y-coordinates of the closest location of the near feature will be written to the X_{Feature Class Name} and Y_{Feature Class Name}  fields.</SPAN></P><P><SPAN>NO_LOCATION נLocation information will not be written to the output table. This is the default.</SPAN></P><P><SPAN>LOCATION נLocation information will be written to the output table.</SPAN></P><P><SPAN /></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Angle (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Specifies whether the near angle will be calculated and written to a NEAR_ANGLE field in the output table. A near angle measures direction of the line connecting an input feature to its nearest feature at their closest locations. When the PLANAR method is used in the method parameter, the angle is within the range of -180Рto 180Ь with 0Рto the east, 90Рto the north, 180Р(or -180Щ to the west, and -90Рto the south. When the GEODESIC method is used, the angle is within the range of -180Рto 180Ь with 0Рto the north, 90Рto the east, 180Р(or -180Щ to the south, and -90Рto the west.</SPAN></P><P><SPAN>NO_ANGLE ؔhe near angle values will not be written. This is the default.</SPAN></P><P><SPAN>ANGLE ؔhe near angle values will be written to the ANGLE_{Feature Class Name}  field.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">Boolean</td>
</tr>
<tr>
<td class="info">Method (Optional) </td>
<td class="info" align="left">
<span style="font-weight: bold">Dialog Reference</span><br /><DIV STYLE="text-align:Left;"><DIV><P><SPAN>Determines whether to use a shortest path on a spheroid (geodesic) or a flat earth (planar) method. It is strongly suggested to use the Geodesic method with data stored in a coordinate system that is not appropriate for distance measurements (for example, Web Mercator or any geographic coordinate system) and any analysis that spans a large geographic area.</SPAN></P><P><SPAN>PLANAR ؕses planar distances between the features. This is the default.</SPAN></P><P><SPAN>GEODESIC ؕses geodesic distances between features. This method takes into account the curvature of the spheroid and correctly deals with data near the dateline and poles.</SPAN></P></DIV></DIV><p><span class="noContent">There is no python reference for this parameter.</span></p></td>
<td class="info" align="left">String</td>
</tr>
</tbody>
</table>
