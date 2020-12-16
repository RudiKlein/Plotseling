import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

""" In Section 1, we’re loading our libraries. We’ll be making use of Pandas and Matplotlib for this
tutorial.In Section 2, we read in the data into a dataframe df, and then select only the countries in our list countries.
Selecting the data makes the resulting visualization a little more readable. In Section 3, we create a summary column that
aggregates the total number of cases across our confirmed cases, recovered cases, and any individuals who have died as a
result of COVID-19."""

""" In Section 4, we pivot our dataframe df, creating columns out of countries, with the number of cases as the data 
fields.This new dataframe is called covid. We then set the index of the dataframe to be the date and assign the country 
names to column headers. In Section 5, we copy our dataframe covid and call it percapita. We use a dictionary that is 
storing all our countries’ populations and divide each value by the population and multiply it by 100,000 to generate a 
number of cases per 100,000 people."""

""" In Section 6, we created a dictionary that contains hex values for different countries. Storing this in a dictionary 
will allow us to easily call it later in a for-loop. We also assign the FiveThirtyEight style to add some general 
formatting, which we’ll heavily build upon. In Section 7, we create our first visualization using Pandas’ plot function. 
We use the colors parameter to assign the colors to different columns. We also use the set_major_formatter method to format
values with separators for thousands. Then, in Section 8, we create a for-loop that generates label text for the various 
countries. This for-loop gets each country’s name from the keys in the dictionary in the form of a list and iterates over 
this list. It places text containing the country’s name to the right of the last x-value (covid.index[-1] → the last date 
in the dataframe), at the current day’s y-value (which will always be equal to the max value of that column). Finally, in 
Section 9, we add a title, subtitle, and source information about the chart. We use variables again to position the data 
so as the graph updates these positions are updated dynamically! """

""" In Section 10, we create another view 
"""

# Section 1 - Loading our Libraries
# https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less-affc361b2c6a
# %matplotlib inline #if you're working in a Jupyter notebook

# Section 2 - Loading and Selecting Data
df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                 parse_dates=['Date'])
countries = ['Netherlands', 'Belgium', 'United Kingdom', 'US']
df = df[df['Country'].isin(countries)]

# Section 3 - Creating a Summary Column
df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)

# Section 4 - Restructuring our Data
df = df.pivot(index='Date', columns='Country', values='Cases')
countries = list(df.columns)
covid = df.reset_index('Date')
covid.set_index(['Date'], inplace=True)
covid.columns = countries

# Section 5 - Calculating Rates per 100,000
populations = {'Netherlands': 17231624, 'Belgium': 11433256, 'United Kingdom': 67802690, 'US': 330548815}
percapita = covid.copy()
for country in list(percapita.columns):
    percapita[country] = percapita[country] / populations[country] * 100000

# Section 6 - Generating Colours and Style
colors = {'Belgium': '#045275', 'Netherlands': '#089099', 'US': '#DC3977',
          'United Kingdom': '#7C1D6F'}
plt.style.use('fivethirtyeight')

# Section 7 - Creating the Visualization
plot = covid.plot(figsize=(20, 8), color=list(colors.values()), linewidth=1, legend=False)
plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plot.grid(color='#d4d4d4')
plot.set_xlabel('Date')
plot.set_ylabel('# of Cases')

# Section 8 - Assigning Colour
for country in list(colors.keys()):
    plot.text(x=covid.index[-1], y=covid[country].max(), color=colors[country], s=country, weight='bold')

# Section 9 - Adding Labels
plot.text(x=covid.index[1], y=int(covid.max().max()) + 45000, s="COVID-19 Cases by Country", fontsize=23, weight='bold',
          alpha=.75)
plot.text(x=covid.index[1], y=int(covid.max().max()) + 15000,
          s="",
          fontsize=16, alpha=.75)
plot.text(x=percapita.index[1], y=-100000,
          s='',
          fontsize=10)

percapitaplot = percapita.plot(figsize=(20, 8), color=list(colors.values()), linewidth=1, legend=False)
percapitaplot.grid(color='#d4d4d4')
percapitaplot.set_xlabel('Date')
percapitaplot.set_ylabel('# of Cases per 100,000 People')

# Section 10 -  second view
for country in list(colors.keys()):
    percapitaplot.text(x=percapita.index[-1], y=percapita[country].max(), color=colors[country], s=country,
                       weight='bold')
percapitaplot.text(x=percapita.index[1], y=percapita.max().max() + 25, s="Per Capita COVID-19 Cases by Country",
                   fontsize=23, weight='bold', alpha=.75)
percapitaplot.text(x=percapita.index[1], y=percapita.max().max() + 10,
                   s="",
                   fontsize=16, alpha=.75)
percapitaplot.text(x=percapita.index[1], y=-55,
                   s='',
                   fontsize=10)
plt.show()
