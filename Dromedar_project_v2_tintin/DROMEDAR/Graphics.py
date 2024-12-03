# VISUALIZATION LIBARIES
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MultipleLocator

def plotting(variable):
    '''
    Just a plotting function based on xarray graphics and the addition of borders
    inside the cartopy library

    Returns
    -------
    Plot

    '''
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    levels=20 #colorbar resolution
    contour = ax.contourf(variable['longitude'], variable['latitude'], variable[0],
                          levels=levels,cmap='viridis', transform=ccrs.PlateCarree())
    plt.colorbar(contour, ax=ax, orientation='vertical', label='Prec mm/day')
    
    # Introducing the boudary of the continent and costlines
    ax.add_feature(cfeature.COASTLINE, linewidth=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=1)
    
    # Just some adjustment of grid and label
    gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, 
                      y_inline=False,color = "None")
    gl.xlocator = MultipleLocator(5)
    gl.ylocator = MultipleLocator(2)
    gl.right_labels = False
    gl.top_labels = False
    
    plt.title('Precipitation:')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.plot()
