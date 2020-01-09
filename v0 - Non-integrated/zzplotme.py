import pandas as pd
#import plotly as py 
import plotly.graph_objs as go

smawindow = 100
mainlineopacity = 0.3

df = pd.read_csv("zscoresv2.csv")
x = df['Generation']

rollavg = df['Current Average'].rolling(window=int(smawindow/5)).mean()
rollhigh = df['Current High'].rolling(window=int(smawindow/5)).mean()


muts = go.Scatter(
	x=x, 
	y=df['Mutations'],
	name='Mutations',
	yaxis='y2',
	mode='markers',
	opacity=0.5,
	marker=dict(
		color='green',
		size=5
		)
	)

size = go.Scatter(
	x=x, 
	y=df['Size'],
	name='Size',
	yaxis='y2',
	mode='markers',
	opacity=0.5,
	marker=dict(
		color='yellow',
		size= 5
		)
	)

inequity = go.Scatter(
	x=x, 
	y=df['Inequity'],
	name='Inequity',
	yaxis='y2',
	mode='markers',
	opacity=0.5,
	marker=dict(
		color='purple',
		size= 5
		)
	)

avg = go.Scatter(
	x=x, 
	y=df['Current Average'],
	name='Current Average',
	opacity = mainlineopacity
	)

high = go.Scatter(
	x=x, 
	y=df['Current High'],
	name='Current High',
	opacity = mainlineopacity
	)

avgSMA = go.Scatter(
	x=x, 
	y=rollavg,
	name='{}SMA, Avg'.format(smawindow),
	line=dict(color='black')
	) 

highSMA = go.Scatter(
	x=x, 
	y=rollhigh,
	name='{}SMA, High'.format(smawindow),
	line=dict(color='black')
	)

data = [avg, high, avgSMA, highSMA, muts, size, inequity]

layout = go.Layout(
    xaxis=dict(
    	title='Generations'
    	),
    yaxis=dict(
        title='Score'
    	),
    yaxis2=dict(
        title='Tuning Variables',
        overlaying='y',
        side='right',
        showgrid = False
    	)
	)

fig = go.Figure(data=data, layout=layout)
fig.show()
