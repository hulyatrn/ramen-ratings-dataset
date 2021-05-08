
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt    
import seaborn as sns   
import random    
import os
for dirname, _, filenames in os.walk('veri/veriler'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

ramen_data = pd.read_csv('ramen-ratings.csv')

ramen_data.head()

ramen_data.describe(include='all')
print(ramen_data['Stars'].describe())

ramen_data['Stars'] = pd.to_numeric(ramen_data['Stars'], errors = 'coerce')
ramen_data.describe(include='all')

ramen_data['Brand'] = ramen_data['Brand'].str.lower()
ramen_data.head()

ramen_brand = ramen_data.groupby(['Brand','Country']).agg({'Review #':'count'})
ramen_brand = ramen_brand.reset_index() 
ramen_brand = ramen_brand.sort_values('Review #', ascending = False)


ramen_coun = ramen_brand.groupby('Country').agg({'Brand':'count'}).reset_index()
ramen_coun = ramen_coun.rename(columns = {'Brand':'Amount of brand'})
ramen_coun = ramen_coun.sort_values(['Amount of brand', 'Country'], ascending = [False, True])

ramen_coun.head(10)

plt.figure(figsize=(15, 5))
plt.bar('Country', 'Amount of brand', data = ramen_coun, color = 'gold')
plt.title( 'The amount of ramen brands in each country', fontsize=14)
plt.ylabel('Number of brands')
plt.xticks(rotation = 90)
plt.show()

ramen_variety = ramen_data.groupby(['Country']).agg({'Variety':'count'})
ramen_variety = ramen_variety.reset_index() 
ramen_variety = ramen_variety.sort_values(['Variety','Country'], ascending = [False, True])
ramen_variety = ramen_variety.rename(columns = {'Variety': 'Country variety'})


plt.figure(figsize=(15, 5))
plt.bar('Country', 'Country variety', data = ramen_variety, color = 'peru')
plt.title( 'The amount of ramen product in each country', fontsize=14)
plt.ylabel('Number of product')
plt.xticks(rotation = 90)
plt.show()

ramen_style = ramen_data.groupby(['Country','Style']).agg({'Variety':'count'})
ramen_style = ramen_style.reset_index()
ramen_style.head()

style_name = sorted(ramen_style['Style'].unique())
print(style_name)

pattern = pd.DataFrame({'dummie' : [0]*266}, \
                       index = pd.MultiIndex.from_product([ramen_coun['Country'], style_name], \
                       names = ['Country', 'Style']))
ramen_style = pd.merge(ramen_style, pattern, how='outer', on=['Country', 'Style'])
ramen_style = ramen_style[['Country', 'Style', 'Variety']].fillna(0)


ramen_style = pd.merge(ramen_style, ramen_variety, how = 'left', on = 'Country')
ramen_style =ramen_style.sort_values(['Country variety','Country', 'Style'], ascending = [False,True, True])

plt.figure(figsize=(15, 5))
bottom_bar = [0]*38 
bar_color = ['chocolate', 'yellowgreen', 'orange', 'forestgreen', 'peru', 'gold', 'saddlebrown']

for i in range(len(style_name)):
    plt.bar('Country', 'Variety', data = ramen_style[ramen_style['Style'] == style_name[i]], \
            bottom = bottom_bar, color = bar_color[i])
    bottom_bar = list(np.add(bottom_bar, ramen_style[ramen_style['Style'] == style_name[i]]['Variety']))

plt.title( 'The amount of ramen style in each country', fontsize=14)
plt.ylabel('Number of ramen')
plt.xticks(rotation = 90)
plt.legend(style_name)
plt.show()


ramen_per = ramen_style[ramen_style['Country variety'] >= 50].reset_index()

ramen_per['Percentage'] = ramen_per['Variety'] * 100 / ramen_per['Country variety']

plt.figure(figsize=(14, 5))
bottom_bar = [0]*12 
for i in range(len(style_name)):
    plt.bar('Country', 'Percentage', data = ramen_per[ramen_per['Style'] == style_name[i]], \
            bottom = bottom_bar, color = bar_color[i])
    bottom_bar = list(np.add(bottom_bar, ramen_per[ramen_per['Style'] == style_name[i]]['Percentage']))

plt.title('The percentage of ramen style in countries which have more than or equal to 50 products reviewed', \
          fontsize=14)
plt.ylabel('Per cent')
plt.xticks(rotation = 90)
plt.legend(style_name,bbox_to_anchor=(1.1, 1))   
plt.show()

ramen_stars = ramen_data.groupby(['Country','Brand']).agg({'Stars': ['mean', 'median'], 'Review #': 'count'})
ramen_stars = ramen_stars.reset_index()
ramen_stars.columns = ['Country','Brand','Mean Stars', 'Median Stars', 'Review#']
ramen_stars = ramen_stars.sort_values('Median Stars', ascending = False)


ramen_stars['Country Brand'] = ramen_stars['Brand'] + ' (' + ramen_stars['Country'] + ')'
ramen_stars.head()

ramen_stars_re = ramen_stars[ramen_stars['Review#'] >= 10].reset_index()
ramen_stars_re = ramen_stars_re.sort_values('Mean Stars', ascending = False)
ramen_stars_re.head()

ramen_stars_re.tail()

ramen_stars_re = ramen_stars_re.sort_values('Median Stars', ascending = False)


ramen_box = ramen_data[['Country','Brand','Stars']].reset_index()
ramen_box['Country Brand'] = ramen_box['Brand'] + ' (' + ramen_box['Country'] + ')'

# Select only brand in country that in ramen_stars_re
ramen_box = ramen_box[ramen_box['Country Brand'].isin(ramen_stars_re['Country Brand'])]

# Create boxplot
fig, ax = plt.subplots(figsize=(5, 20))
sns.boxplot(x = 'Stars', y = 'Country Brand', data = ramen_box, color = 'yellow',\
            order = ramen_stars_re['Country Brand'], showmeans = True,\
            meanprops = {'marker': 'o','markerfacecolor': 'saddlebrown', 'markeredgecolor': 'saddlebrown'})
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top') 
plt.title( 'The distribution of the stars in each brand (mean display as brown circles)', \
          fontsize=14)
plt.show()
