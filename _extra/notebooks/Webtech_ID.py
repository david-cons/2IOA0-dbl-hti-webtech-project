import numpy as np
import pandas as pd

# next command ensures that plots appear inside the notebook
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults
plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

# reveal a hint only while holding the mouse down
from IPython.display import HTML
HTML("<style>.h,.c{display:none}.t{color:#296eaa}.t:active+.h{display:block;}</style>")

# hide FutureWarnings, which may show for Seaborn calls in most recent Anaconda
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

df_enron = pd.read_csv('enron-v1.csv')

Person_ID_1 = 68
person_send = df_enron['fromId'] == Person_ID_1
person_received = df_enron['toId'] == Person_ID_1
df_1 = df_enron[person_send]
df_2 = df_1[['fromEmail']]
df_3 = df_2.describe()
ID_mail = df_3['fromEmail']['top']
df_describe_person = df_enron[person_send][['fromJobtitle']].describe()
job_title = df_describe_person['fromJobtitle']['top']
mails_send = df_enron[person_send]['sentiment'].count()
mean_sentiment_send = df_enron[person_send]['sentiment'].mean()
min_sentiment_send = df_enron[person_send]['sentiment'].min()
max_sentiment_send = df_enron[person_send]['sentiment'].max()
mails_received = df_enron[person_received]['sentiment'].count()
mean_sentiment_received = df_enron[person_received]['sentiment'].mean()
min_sentiment_received = df_enron[person_received]['sentiment'].min()
max_sentiment_received = df_enron[person_received]['sentiment'].max()

#Person_ID_1, ID_mail, job_title, mails_send, mean_sentiment_send, min_sentiment_send, max_sentiment_send, mails_received, mean_sentiment_received, min_sentiment_received, max_sentiment_received

# df_person_send_1 = df_enron[person_send].groupby('toId').describe()
# df_person_send_2 = df_person_send_1['fromId']
# df_person_send = df_person_send_2[['count']]
# df_person_send #All ID nmbrs Person_ID send mails to, and the number of mails he send to that ID