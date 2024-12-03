# AUTHOR
- Battisti Mattia [MSc Environmental Meteorology](University of Trento)

# DROMEDAR

The project purpose is to prepare an overall time series that will be use to characterise the drought events and the possible
scenarios combining the SMILEs models for future projections.
But before it is necessary to understand how to characterise past drought and how this characterisation will change under climate
change and understand what are the factors that amplify the drought events. A first step analyse ERA5 reanalysis and with the
meteorological variables Z500, IVT, Thermodynamic variables (qv, RH, Ts) and Solar radiation characterise and access the past and historical droughts. This access
can be helped calculatind drought indexes such SPI, SPEI and RDI that combined allow to calculate a more robust index to access drougths.
Correlation analysis is a crucial point that allows to understand if meteorological variables and droughts indexes are consistent with physics.
Then this idendical analysis can be transposed on large ensemble to understand future projections of drought.

# DROMEDAR (Droughts of Mediterrenean regions) Project CODE

The project script is structured in multiple modules that contains different functionality in order to simplify the readability,
and allow to add modules from other developers without breaking the main function of the program.
The modules are:

    1 - DROMEDAR OPERATORS
        - complete_timeseries [Battisti Mattia] -> function that avoid to jump the initial data if we work with
                                                    runsum, runmean, ...                       
        - mon_sum [Battisti Mattia] -> calculates the sum the variable for all the day of the month;
        - magnitude [Battisti Mattia] -> calculates the magnitude of the vectorial sum;
        - SPI_len [Battisti Mattia](Ref.Jacopo Brida) -> calculates the SPI starting from daily total precipitation;
	- SPI_len [Battisti Mattia] -> calculates the SPEI starting from daily budget between total precipitation and PET;
        - SPI_len [Battisti Mattia](Ref.Jacopo Brida) -> calculates the RDI starting from daily ratio between total preciprecipitation and PET;
        - remapping_tmpl [Battisti Mattia] -> it creates a template from topography at the resolution given and can be used to remap
                                              another file.nc;
        - remapping [Battisti Mattia] -> it uses the remapping template and apply the new resolution taken from the remapping template 
 
    2 - GRAPHICS
        - plotting

    3 - FILE TOOLS
        - list_files [Battisti Mattia] -> return a list of the file inside the folder given by the user
        - choose_file [Battisti Mattia] -> allows the user to choose wich file he wants to use
        - infos [Battisti Mattia] -> shows the info of the file using cdo package
        - delater [Battisti Mattia] -> allows to delate files giving the file path
        - command_run_tested -> runs the command choose by the user
	
    4 - VAR REMAP OPTIONS 
        - variables_remapping [Battisti Mattia] -> function that allows to insert the variable in verbous way that the user can
                                                    include and remap as wish
 
    5 - MAIN
    	It is just the module allows to run the entire packages together and that is interactive and allow the user to choose what
    	he want to do (i.e. SPI calculation, remapping, ...)

## SPI
The SPI is a drought index developed by McKee 1993 that allows to calculate the precipitation anomaly respect to the mean of the timeseries (runmean).
It can be adapted to different time span that depend on the drought type (meteorological, climatological, hydrological, socio-economical and agricoltural).
This distinction become very powerful in decision making and allows to understand in an easier way to define the magnitude of the drought extreme events.

The package can calculate the SPI starting from the daily precipitation data, but with slightly modification
it can be adapt eventually to other time steps. This calculation approach is based on the observation and
the percentiles are defined with critical values. 
If the idea is to calculate the modelled SPI from the modelled precipitation this approach maybe it wont
work as for the observed values of precpitation.

	OPERATIONAL DETAILS
		- The total precipitation file in the folder needs to be called as MODELNAME_OTHERDETAILS.nc, because MODELNAME
			is used to name the final outputs;
		- Inside the function i.e. IMERG is separated from the other models because the different timesteps that stars
			from 19/06/2000 and i.e. CERRA and ERA5 from 01/01/2000. For this reason it can be modified as wish;
		- Because the attributes changes in function of the file generated (i.e. SPI variable is dimensionless) the measure
			units will be unphysical. For this reason total precipitation variable could be different for the different
			models, so the variable var=str(variable_name) (i.e. IMERG var=str(pr); ERA5 and CERRA var=str(tp));
		- Other detail can be found using $ cdo.sinfon() or from the command line $ ncdump -h file.nc.

## SPEI
But the SPI index does not considers the evaporation and so the temperature and the energy flux given by the sensible and latent heat, so that SPEI comes in.
The SPEI index developed by Vicent Serrato 1997 allows to includes the effect of PET (potential evapotraspiration). The calculation procedure is the same as the SPI 
but in the end the results instead of precipitation anomaly indicates the budget anomaly. In this specific case ERA5 gives PET datasets that comes from the
equation of Pennmn-Monteith or Hargreaves-Samani.

N.B. Negative values of PET are intended as output from the surface and so - upward that is consisten with the + sign of input water given by the precipitation,
so precipitation must be summed to the PET.

The package can calculate the SPEI starting from the daily budget between total precipitation and PET data (tp - PET), but with slightly modification
it can be adapt eventually to other time steps. This calculation approach is based on the observation and
the percentiles are defined with critical values.

        OPERATIONAL DETAILS
                - The total precipitation minus PET file in the folder needs to be called as MODELNAME_OTHERDETAILS.nc, because MODELNAME
                        is used to name the final outputs;
                - Because the attributes changes in function of the file generated (i.e. SPEI variable is dimensionless) the measure
                        units will be unphysical. For this reason total precipitation variable could be different for the different
                        models, so the variable var=str(variable_name) (i.e. IMERG var=str(pr); ERA5 and CERRA var=str(tp)) (NOT INCLUDED IN SPEI);
                - Other detail can be found using $ cdo.sinfon() or from the command line $ ncdump -h file.nc.

## RDI
The RDI index developed by G.Tsakiris et.al 2007, similarly to SPI and SPEI allows to calculate something related to the drought. What is considered is a ratio
between total precipitation and PET that allows us to understand the drought severity. 

The package can calculate the RDI starting from the daily ratio between total precipitation and PET data (tp//PET), but with slightly modification
it can be adapt eventually to other time steps. This calculation approach is based on the observation and
the percentiles are defined with critical values.

        OPERATIONAL DETAILS
                - The total precipitation divided PET file in the folder needs to be called as MODELNAME_OTHERDETAILS.nc, because MODELNAME
                        is used to name the final outputs;
                - Because the attributes changes in function of the file generated (i.e. SPEI variable is dimensionless) the measure
                        units will be unphysical. For this reason total precipitation variable could be different for the different
                        models, so the variable var=str(variable_name) (i.e. IMERG var=str(pr); ERA5 and CERRA var=str(tp)) (NOT INCLUDED IN RDI);
                - Other detail can be found using $ cdo.sinfon() or from the command line $ ncdump -h file.nc.

# COMBINED INDEX
SPI, SPEI and RDI can be merged togheter in a single drought index that becomes stronger and more consistent and allows us to give a global prospective
on the drought events. This approach can be found in literature, the paper that I reffered to apply this approach is by Spinoni et.al 2017

## HOW TO RUN IT?

1 - Make sure you have all dependencies installed. These are:
        - os
        - subprocess
        - cdo (https://code.mpimet.mpg.de/attachments/download/27273/python_cdo_introduction.pdf)
        - xarray
        - netCDF4
        - numpy
        - matplotlib
        - cartopy
        
2 - Inside the modules make sure that the file and folder path are the one of the your pc

3 - Once the main file is running you have to follow instructions and select file if necessary

4 - Actually if you press no when the program asks if you want to calculate SPI is just the script still in develop

