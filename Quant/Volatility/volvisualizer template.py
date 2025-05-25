from volvisualizer.volatility import Volatility
imp = Volatility(ticker='^SPX', start_date='2023-11-29', wait=0.5, monthlies=True, q=0.013)

imp.visualize(graphtype='line')


#3D scatter plot
imp.visualize(graphtype='scatter', voltype='ask', months=6)

#3D wireframe plot
imp.visualize(graphtype='surface', surfacetype='spline', scatter=True, smoothing=True)

#3D Mesh Grid
imp.visualize(graphtype='surface', surfacetype='mesh', smoothing=True)

#3D interactive grid
imp.visualize(graphtype='surface',surfacetype='interactive_spline', smoothing=True, notebook=False, colorscale='Blues', scatter=True, opacity=0.8)

#3D Interactive plot of each option implied volatility by strike and expiry using radial basis function interpolation.
imp.visualize(graphtype='surface', surfacetype='interactive_spline', rbffunc='cubic', colorscale='Jet', smoothing=True)

#extract Implied Volatitlity for date and strike
imp.vol(maturity='2023-09-30', strike=80)

#downside skew summary report
imp.skewreport(months=12, direction='down')

#upside skew report
imp.skewreport(months=9, direction='up')

#upside and downside skew report
imp.skewreport(months=15, direction='full')