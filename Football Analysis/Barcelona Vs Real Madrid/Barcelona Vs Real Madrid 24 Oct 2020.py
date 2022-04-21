#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from mplsoccer.pitch import Pitch, VerticalPitch
from statsbombpy import sb
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[2]:


sb.competitions()


# In[3]:


matches = sb.matches(competition_id=11, season_id=90)


# In[4]:


matches[matches['home_team'] == 'Barcelona']


# In[5]:


events = sb.events(match_id=3773585)


# In[6]:


events.head()


# In[7]:


events.columns


# In[8]:


columns = ['team', 'player', 'player_id', 'minute', 'location', 'pass_end_location', 'type', 'pass_outcome', 'shot_statsbomb_xg', 'shot_outcome']
events = events[columns]


# In[9]:


pass_events = events[events['type'] == 'Pass'].reset_index()


# In[10]:


pass_events['pass_outcome'] = pass_events['pass_outcome'].fillna('Complete')


# In[11]:


x = []
y = []
x_end = []
y_end = []
for i in range(len(pass_events['location'])):
    x.append(pass_events['location'][i][0])
    y.append(pass_events['location'][i][1])
    
for i in range(len(pass_events['pass_end_location'])):
    x_end.append(pass_events['pass_end_location'][i][0])
    y_end.append(pass_events['pass_end_location'][i][1])


# In[12]:


pass_events['x'] = x
pass_events['y'] = y
pass_events['x_end'] = x_end
pass_events['y_end'] = y_end


# In[13]:


pass_events = pass_events.drop(['location', 'pass_end_location'], axis=1)


# In[14]:


pass_events[pass_events['team'] == 'Barcelona']


# In[15]:


pass_events.info()


# In[16]:


fig, ax = plt.subplots(figsize=(13,10), ncols=2, nrows=1)
pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='grass', stripe=True, 
              orientation='horizontal', constrained_layout=True)
pitch.draw(ax=ax[0])
pitch.draw(ax=ax[1])
ax[0].invert_xaxis()
ax[1].invert_xaxis()
ax[1].invert_yaxis()

frenkie = pass_events[pass_events['player'] == 'Frenkie de Jong']
kde = sns.kdeplot(frenkie['y'], frenkie['x'], shade=True, shade_lowest=False, alpha=.5, ax=ax[0],  cmap='magma')

toni = pass_events[pass_events['player'] == 'Toni Kroos']
kde = sns.kdeplot(toni['y'], toni['x'], shade=True, shade_lowest=False, alpha=.5, ax=ax[1])

for i in range(len(pass_events['x'])):
    if pass_events['player'][i] == 'Frenkie de Jong':
        ax[0].scatter(pass_events['y'][i], pass_events['x'][i], color='Blue')
    elif pass_events['player'][i] == 'Toni Kroos':
        ax[1].scatter(pass_events['y'][i], pass_events['x'][i], color='White')


# In[17]:


np.unique(pass_events[pass_events['team'] == 'Barcelona']['player'])


# ## Expected Goals

# In[18]:


xgoals_event = events[events['shot_statsbomb_xg'].notnull()].reset_index()


# In[19]:


xgoals_event.head(10)


# In[20]:


xgoals_event = xgoals_event.drop(['pass_end_location', 'pass_outcome'], axis=1)


# In[21]:


x_shot = []
y_shot = []
for i in range(len(xgoals_event['location'])):
    x_shot.append(xgoals_event['location'][i][0])
    y_shot.append(xgoals_event['location'][i][1])
    
xgoals_event['x'] = x_shot
xgoals_event['y'] = y_shot


# In[22]:


madrid_goals= xgoals_event[xgoals_event['team'] == 'Real Madrid'][xgoals_event['shot_outcome'] == 'Goal'].count()['shot_outcome']
bfc_goals = xgoals_event[xgoals_event['team'] == 'Barcelona'][xgoals_event['shot_outcome'] == 'Goal'].count()['shot_outcome']


# In[23]:


# membuat pitch xGoal
fig, ax = plt.subplots(figsize=(13.5, 8))
fig.set_facecolor('#22312b')
# ax.patch.set_facecolor('#22312b')

pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', 
              pitch_color='grass', line_color='white', stripe=True, figsize=(16,11), constrained_layout=True,
             tight_layout=False, tick=True, label=True)
pitch.draw(ax=ax)
plt.gca().invert_yaxis()
annotation = ax.annotate("Real Madrid "+str(madrid_goals) + " - " + str(bfc_goals) + " Barcelona", (59,70),fontsize=30, ha='center')
plt.title('Barcelona Vs Real Madrid xGoal', color='White', size=20)

for i in range(len(xgoals_event['x'])):
    if xgoals_event['team'][i] == 'Barcelona':
        if xgoals_event['shot_outcome'][i] == 'Goal':
            plt.scatter(xgoals_event['x'][i], xgoals_event['y'][i], color='yellow', s=xgoals_event['shot_statsbomb_xg'][i]*1000)
        else:
            plt.scatter(xgoals_event['x'][i], xgoals_event['y'][i], color='blue', s=xgoals_event['shot_statsbomb_xg'][i]*1000)
    elif xgoals_event['team'][i] == 'Real Madrid':
        if xgoals_event['shot_outcome'][i] == 'Goal':
            plt.scatter((xgoals_event['x'][i]/12), xgoals_event['y'][i], color='yellow', s=xgoals_event['shot_statsbomb_xg'][i]*1000)
        else:
            plt.scatter((xgoals_event['x'][i]/12), xgoals_event['y'][i], color='white', s=xgoals_event['shot_statsbomb_xg'][i]*1000)


# In[ ]:




