import sys, os, Ngl
import numpy as np
import pandas as pd
import xarray as xr
import time as tm
from netCDF4 import Dataset, num2date

#-------------------------------------------------------
# Function to attach lat/lon labels to a Robinson plot
#-------------------------------------------------------
def add_labels_lcm(wks,map,dlat,dlon):
  PI         = 3.14159
  RAD_TO_DEG = 180./PI

#-- determine whether we are in northern or southern hemisphere
  if (float(minlat) >= 0. and float(maxlat) > 0.):
     HEMISPHERE = "NH"
  else:
     HEMISPHERE = "SH"




#-- pick some "nice" values for the latitude labels.
  lat_values = np.arange(int(minlat+5),int(maxlat),10)
  #lat_values = lat_values.astype(float)
  nlat       = len(lat_values)

#-- We need to get the slope of the left and right min/max longitude lines.
#-- Use NDC coordinates to do this.
  lat1_ndc = 0.
  lon1_ndc = 0.
  lat2_ndc = 0.
  lon2_ndc = 0.
  lon1_ndc,lat1_ndc = Ngl.datatondc(map,minlon,lat_values[0])
  lon2_ndc,lat2_ndc = Ngl.datatondc(map,minlon,lat_values[nlat-1])
  slope_lft         = (lat2_ndc-lat1_ndc)/(lon2_ndc-lon1_ndc)

  lon1_ndc,lat1_ndc = Ngl.datatondc(map,maxlon,lat_values[0])
  lon2_ndc,lat2_ndc = Ngl.datatondc(map,maxlon,lat_values[nlat-1])
  slope_rgt         = (lat2_ndc-lat1_ndc)/(lon2_ndc-lon1_ndc)
  
#-- set some text resources
  txres               = Ngl.Resources()
  txres.txFontHeightF = 0.018
  txres.txPosXF       = 0.1

#-- Loop through lat values, and attach labels to the left and right edges of
#-- the masked LC plot. The labels will be rotated to fit the line better.
  dum_lft       = []                            #-- assign arrays
  dum_rgt       = []                            #-- assign arrays
  lat_label_lft = []                            #-- assign arrays
  lat_label_rgt = []                            #-- assign arrays

  for n in range(0,nlat):
#-- left label
    if(HEMISPHERE == "NH"):
       rotate_val = -90.
       direction  = "N"
    else:
       rotate_val =  90.
       direction  = "S"

#-- add extra white space to labels
    lat_label_lft.append("{}~S~o~N~{}              ".format(str(np.abs(lat_values[n])),direction))
    lat_label_rgt.append("              {}~S~o~N~{}".format(str(np.abs(lat_values[n])),direction))
        
    txres.txAngleF = RAD_TO_DEG * np.arctan(slope_lft) + rotate_val
                             
  #  dum_lft.append(Ngl.add_text(wks,map,lat_label_lft[n],minlon,lat_values[n],txres))

#-- right label
    if(HEMISPHERE == "NH"):
       rotate_val =  90
    else:
       rotate_val = -90

    txres.txAngleF = RAD_TO_DEG * np.arctan(slope_rgt) + rotate_val

    dum_rgt.append(Ngl.add_text(wks,map,lat_label_rgt[n],maxlon,lat_values[n],txres))

#----------------------------------------------------------------------
# Now do longitude labels. These are harder because we're not adding
# them to a straight line.
# Loop through lon values, and attach labels to the bottom edge for
# northern hemisphere, or top edge for southern hemisphere.
#----------------------------------------------------------------------
  del(txres.txPosXF)
  txres.txPosYF = -5.0

#-- pick some "nice" values for the longitude labels
  #lon_values = np.arange(int(minlon+10),int(maxlon-10),10).astype(float)
  lon_values = np.arange(int(minlon+5),int(maxlon),10) #.astype(float)
  lon_values = np.where(lon_values > 180, 360-lon_values, lon_values)
  nlon       = lon_values.size

  dum_bot    = []                            #-- assign arrays
  lon_labels = []                            #-- assign arrays

  if(HEMISPHERE == "NH"):
     lat_val    = minlat
  else:
     lat_val    = maxlat

  ctrl = "~C~"

  for n in range(0,nlon):
    if(lon_values[n] < 0):
       if(HEMISPHERE == "NH"):
          lon_labels.append("{}~S~o~N~W{}".format(str(np.abs(lon_values[n])),ctrl))
       else:
          lon_labels.append("{}{}~S~o~N~W".format(ctrl,str(np.abs(lon_values[n]))))
    elif(lon_values[n] > 0):
       if(HEMISPHERE == "NH"):
          lon_labels.append("{}~S~o~N~E{}".format(str(lon_values[n]),ctrl))
       else:
          lon_labels.append("{}{}~S~o~N~E".format(ctrl,str(lon_values[n])))
    else:
       if(HEMISPHERE == "NH"):
          lon_labels.append("{}0~S~o~N~{}".format(ctrl,ctrl))
       else:
          lon_labels.append("{}0~S~o~N~{}".format(ctrl,ctrl))

#-- For each longitude label, we need to figure out how much to rotate
#-- it, so get the approximate slope at that point.
    if(HEMISPHERE == "NH"):             #-- add labels to bottom of LC plot
       lon1_ndc,lat1_ndc = Ngl.datatondc(map, lon_values[n]-0.5, minlat)
       lon2_ndc,lat2_ndc = Ngl.datatondc(map, lon_values[n]+0.5, minlat)
       txres.txJust = "TopCenter"
    else:                               #-- add labels to top of LC plot
       lon1_ndc,lat1_ndc = Ngl.datatondc(map, lon_values[n]+0.5, maxlat)
       lon2_ndc,lat2_ndc = Ngl.datatondc(map, lon_values[n]-0.5, maxlat)
       txres.txJust = "BottomCenter"

    slope_bot = (lat1_ndc-lat2_ndc)/(lon1_ndc-lon2_ndc)
    txres.txAngleF  =  RAD_TO_DEG * np.arctan(slope_bot)
    
#-- attach to map
    dum_bot.append(Ngl.add_text(wks, map, str(lon_labels[n]), \
                                lon_values[n], lat_val, txres))
  return

############################################################################
######## MAIN
hem='N'

model = sys.argv[1]; hem = sys.argv[2]; thr_label = sys.argv[3]
period = sys.argv[4] ; seas = sys.argv[5] ; nlabel = sys.argv[6]

#nlabel = '{}At'.format(hem)
dirin = './{}/{}/{}/STATS/scl'.format(model,thr_label,nlabel)
dirout = './{}/{}/{}/FIG/STATS'.format(model,thr_label,nlabel)

os_status = os.system("mkdir -p {}".format(dirout)) 

if seas != 'none':
	fname_mean = '{}/stat_scl_{}_mean_{}{}.nc'.format(dirin,nlabel,period,seas)
	fname_std = '{}/stat_scl_{}_std_{}{}.nc'.format(dirin,nlabel,period,seas)
	fsave = '{}/stat_scl_{}_{}{}'.format(dirout,nlabel,period,seas)
	print('entrou')
else:
	fname_mean = '{}/stat_scl_{}_mean_{}.nc'.format(dirin,nlabel,period)
	fname_std = '{}/stat_scl_{}_std_{}.nc'.format(dirin,nlabel,period)
	fsave = '{}/stat_scl_{}_{}'.format(dirout,nlabel,period)

if hem == "S":
	minlon = -75.
	minlat = -70.
	maxlon = 25.
	maxlat = -15.
else:
	minlon  = -120.#-85. 
	minlat  = 25.  
	maxlon  = 5.  
	maxlat  = 80.  

# open file
# ds_mean = xr.open_dataset(fname_mea, engine='pynio') 
ds_mean = xr.open_dataset(basefilename + wwvc) 
ds_std = xr.open_dataset(fname_std, engine='pynio') 

var1 = ds_mean.variables['Hs']
lon = ds_mean.coords['longitude'] 
lat = ds_mean.coords['latitude']

#---------------------------------------------------
# ------- plot (Ngl).

wks_type = "png"
wks = Ngl.open_wks(wks_type,"ngl01p")

cnres                 = Ngl.Resources()
cnres.nglFrame        = False
# Contour resources
cnres.cnFillOn        = True
cnres.cnFillPalette   = "WhiteBlueGreenYellowRed" #"CBR_wet"       
cnres.cnLinesOn       = False
cnres.cnLineLabelsOn  = False
cnres.cnLevelSelectionMode   = "ManualLevels"
cnres.cnMinLevelValF         = 0.2#0.1
cnres.cnMaxLevelValF         = 6.#3.
cnres.cnLevelSpacingF         = 0.2#0.1

# label options
cnres.lbOrientation   = "horizontal"
cnres.lbLabelFontHeightF = 0.014
cnres.tmXBLabelFontHeightF = 0.014
cnres.tmYLLabelFontHeightF = 0.014
#cnres.lbTitleString        = "" # bar title
#cnres.lbTitlePosition      = "Bottom" 
#cnres.lbTitleJust = "TopRight"  
#cnres.lbTitleFontHeightF   = 0.02  

# Regional Map - Lambert 
#cnres.tiMainOffsetYF         =  0.05
#cnres.tiMainFontHeightF      =  0.016                   #-- decrease font size

cnres.mpProjection           = "LambertConformal"
cnres.nglMaskLambertConformal = True                    #-- turn on lc masking
cnres.mpLambertParallel1F    =  10
cnres.mpLambertParallel2F    =  70
cnres.mpLambertMeridianF     = -100
cnres.mpLimitMode            = "LatLon"
cnres.mpMinLonF              =  minlon
cnres.mpMaxLonF              =  maxlon
cnres.mpMinLatF              =  minlat
cnres.mpMaxLatF              =  maxlat
cnres.mpGridAndLimbOn        =  True
cnres.mpGridSpacingF         =  5.

cnres.pmTickMarkDisplayMode  = "Always"

# Additional resources needed for putting contours on map
cnres.sfXArray          = lon.data
cnres.sfYArray          = lat.data

# Map resources
cnres.mpFillOn               = False
#cnres.mpFillDrawOrder        = "PostDraw"
#cnres.mpLandFillColor        = "Gray"
cnres.mpOceanFillColor       = "Transparent"
cnres.mpInlandWaterFillColor = "Transparent"
cnres.mpDataBaseVersion      = "MediumRes"
cnres.mpDataSetName          = "Earth..4"
cnres.mpCountyLineColor      = "Black"
#cnres.mpOutlineBoundarySets  = "AllBoundaries"
#cnres.mpFillBoundarySet      = "Brazil"
cnres.mpGeophysicalLineColor = "Black" # Changes the outline line color.
cnres.mpCountyLineColor = "Black"
#cnres.mpNationalLineColor = "Navy"
#cnres.mpProvincialLineColor = "Navy"
cnres.mpGeophysicalLineThicknessF = 3
cnres.mpCountyLineThicknessF = 3
#cnres.mpNationalLineThicknessF = 3
#cnres.mpProvincialLineThicknessF = 3
#cnres.mpGridLatSpacingF      = 5
#cnres.mpGridLonSpacingF      = 5
cnres.mpGridLineDashPattern  = 5 

# 2nd contour (line)
cnres2                 = Ngl.Resources()
cnres2.nglFrame        = False
cnres2.nglDraw         = False
cnres2.cnFillOn        = False     
cnres2.cnLinesOn       = True
cnres2.cnLineLabelsOn  = False
cnres2.cnInfoLabelOn   = False
#cnres2.cnLineLabelInterval = 4
#cnres2.cnLineLabelBackgroundColor = -1
#cnres2.cnLineLabelFontColor = "gray20" 
#cnres2.cnLineLabelFontHeightF = 0.014
#cnres2.cnLabelMasking        = True
cnres2.cnLineDashPatterns        = 3       
cnres2.cnLineThicknessF          = 4 
cnres2.cnLineColor = "gray20"           
cnres2.cnLevelSelectionMode   = "ManualLevels"
cnres2.cnMinLevelValF         = 0.
cnres2.cnMaxLevelValF         = 10.
cnres2.cnLevelSpacingF         = 1.
cnres2.sfXArray          = lon.data
cnres2.sfYArray          = lat.data

contour = Ngl.contour_map(wks,var1[:,:],cnres)
contour2 = Ngl.contour(wks,var1[:,:],cnres2)
tx = add_labels_lcm(wks,contour,5,5)
Ngl.overlay(contour,contour2)
Ngl.draw(contour)
Ngl.frame(wks)
	
print('end')

#Ngl.end()
