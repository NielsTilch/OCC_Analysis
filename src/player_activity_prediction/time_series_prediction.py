import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX

df = pd.read_csv('csvFiles/time_series_match-period-300s.csv')

number_point=75000
train_slice=0.99


list_activity = df['activity']

plt.plot(list_activity[:int(np.ceil(number_point*train_slice))])

train = list_activity[:int(np.ceil(number_point*train_slice))]
test = list_activity[int(np.ceil(number_point*train_slice)):number_point]

ARMAmodel = SARIMAX(train, order = (1, 0,0))

results = ARMAmodel.fit()

start_forecast = int(np.ceil(number_point*train_slice))
end_forecast = number_point
pred = results.get_prediction(start=start_forecast,end=end_forecast ,dynamic=False)
pred_ci = pred.conf_int()


ax =test.plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='Predictions', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Time')
ax.set_ylabel('Number of players')
plt.legend()

plt.show()