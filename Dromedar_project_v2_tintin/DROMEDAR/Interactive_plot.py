#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:56:01 2024

@author: mattia
"""

def plotting_interactive(variable):
    '''
    A plotting function based on xarray graphics and the addition of borders
    inside the cartopy library with an interactive slider.
    
    NB JUST FOR VISUALIZATION BUGS

    Parameters
    ----------
    variable : xarray.DataArray
        An xarray DataArray with dimensions including 'time', 'lat', and 'lon'.

    Returns
    -------
    None
    '''
    # Convert time to readable dates
    times = variable['time'].values
    dates = mdates.num2date(mdates.date2num(times))
    num_times = len(times)

    # Create the figure and the axis
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
    plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)  # Adjust space for slider

    # Initialize the colorbar and contour variables
    colorbar = None
    contour = None

    def update_plot(time_index):
        """
        Update the plot for the given time index.
        """
        nonlocal colorbar, contour
        
        # Update the data for the current time step
        data = variable.isel(time=time_index)
        vmin = data.min().values
        vmax = data.max().values
        
        # Ensure that levels cover the range of the data
        levels = np.linspace(vmin, vmax, 20)
        
        # Clear the current plot
        ax.clear()
        
        # Plot new contour
        contour = ax.contourf(variable['lon'], variable['lat'], data, 
                              levels=levels, cmap='viridis', transform=ccrs.PlateCarree())
        
        # Add features to the map
        ax.add_feature(cfeature.COASTLINE, linewidth=1)
        ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=1)
        
        # Gridlines and labels
        gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False, color='gray', linestyle='--')
        gl.xlocator = MultipleLocator(5)
        gl.ylocator = MultipleLocator(2)
        gl.right_labels = False
        gl.top_labels = False
        
        # Update title with current date
        ax.set_title(f'Precipitation: {dates[time_index].strftime("%Y-%m-%d")}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        
        # Update colorbar
        if colorbar:
            colorbar.remove()
        colorbar = fig.colorbar(contour, ax=ax, orientation='vertical', label='Prec mm/day')

        fig.canvas.draw_idle()  # Redraw the canvas

    # Add the slider
    ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')
    slider = widgets.Slider(ax_slider, 'Time', 0, num_times - 1, valinit=0, valfmt='%0.0f')

    def on_slider_change(val):
        """
        Update the plot when the slider value changes.
        """
        frame = int(slider.val)
        print(f'Slider value: {frame}')  # Debugging line
        update_plot(frame)

    slider.on_changed(on_slider_change)

    # Initial plot
    update_plot(0)

    plt.show()