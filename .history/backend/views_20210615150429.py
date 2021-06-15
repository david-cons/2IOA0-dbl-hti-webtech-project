from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

from .forms import timeForm
import django.http
import json
import pandas as pd


############Filtering###############
def filterDataByTime(request, data):
    startDate = request.POST.get("start_date", '0000-00-00')
    endDate = request.POST.get("end_date", '9999-99-99')
    return data[ ((data["date"]>=startDate) & (data["date"] <= endDate)) ]

def filterDataByJobtitle(request, data):
    activeJobTitles = []
    
    for i in request.POST.get("activeJobTitles").split():
        activeJobTitles.append(i)

    return data[ data['fromJobtitle'] in activeJobtitles]

def filterDataBySentiment(request,data):
    sentimentValue = True if (request.POST.get("sentiment") == "positive") else False
    return data[(data["sentiment"]>= 0)] if sentimentValue else data[(data["sentiment"] <= 0)]

def filterDataByPerson(request,data): #used for other purposes not necessarily in filtering
    personID = request.POST.get("personID")
    return data[ ( (data["fromId"] == personID) | (data["toId"] == personID) ) ]

def filterDataByEmailAddress(request,data):
    email = request.POST.get("email")
    return data[ ( (data["fromEmail"] == email) | (data["toEmail"] == email) ) ]

"""
def filter(request,data): #full filtering
    data = filterDataByTime(request, data)
    data = filterDataByJobtitle(request, data)
    data = filterDataBySentiment(request, data)
    data = filterDataByEmailAddress(request, data)
    # compound with more filtering options
    
    return data 
"""

def filter(request,data): #full filtering
    finalData = filterDataByTime(request, data)
    #return filterDataByJobtitles(request, finalData) 
    return finalData

################################################################

def index(request):
    return render(request, 'index.html')

def makeGraph(request, df_enron):
    
    import networkx
    import matplotlib.pyplot as plt
    import numpy as np

    #from bokeh.io import output_notebook, show, save
    from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
    from bokeh.plotting import figure
    from bokeh.models.graphs import from_networkx
    from bokeh.palettes import Category10
    from bokeh.transform import linear_cmap
    from bokeh.embed import json_item

    #output_notebook() #remove this when not using notebook

    G = networkx.from_pandas_edgelist(df_enron, 'fromId', 'toId', edge_attr=True)

    di = {'CEO':1,'Director':2,'Employee':3,'In House Lawyer':4,'Manager':5,'Managing Director':6,'President':7,'Trader':8,'Unknown':9,'Vice President':10}
    df_rejob = df_enron.replace({"fromJobtitle": di})
    df_attributes = df_enron[['fromId', 'fromJobtitle']].drop_duplicates()
    df_attributes.columns = ['fromId', 'job']
    df_attributesx = df_rejob[['fromId', 'fromJobtitle']].drop_duplicates()
    job = df_attributes.set_index('fromId').to_dict('i')
    jobx = df_attributesx.set_index('fromId').to_dict('i')
    networkx.set_node_attributes(G, job)
    networkx.set_node_attributes(G, jobx)
    #jobs = ['Employee','Vice President','Unknown','Manager','CEO','Trader','Director','President','Managing Director','In House Lawyer']

    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)
    adjusted_node_size = dict([(node, (degree + 5) - ((degree + 5)*0.3) ) for node, degree in networkx.degree(G)])
    networkx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'fromJobtitle'

    color_palette = Category10[10]

    TOOLTIPS = [
        ("Person ID", "@index"),
            ("people communicated with", "@degree"),
            ("Jobtitle","@job"),
    ]

    graph_size = int(request.POST.get('graph_size', '720'))
    plot = figure(tooltips = TOOLTIPS,
                tools="pan,zoom_in,wheel_zoom,save,reset,box_select,undo", active_scroll='wheel_zoom',
                x_range=Range1d(-20,20), y_range=Range1d(-20,20),  title='Enron Emails',
                plot_width=graph_size, plot_height=graph_size)
    plot.axis.visible = False

    N_graph = from_networkx(G, networkx.spring_layout, scale=100)

    N_graph.node_renderer.glyph = Circle(size=size_by_this_attribute,
                                        fill_color=linear_cmap(color_by_this_attribute, color_palette, 1, 10))

    N_graph.edge_renderer.glyph = MultiLine(line_alpha=10, line_width=1)

    plot.renderers.append(N_graph)

    item_text = json.dumps(json_item(plot))

    return item_text

def fullSizeGraph(request):
    
    graph_json = makeGraph(request, filterDataByTime(request,pd.read_csv(request.FILES['csv_data'])))
    return django.http.JsonResponse(graph_json, safe=False)

def initialFullSizeGraph(request):
    
    df_dataset = pd.read_csv(request.FILES['csv_data'])
    graph_json = makeGraph(request, df_dataset)
    
    startDate = df_dataset["date"].min()
    endDate = df_dataset["date"].max()

    startYear = int(startDate[:4])
    endYear = int(endDate[:4])

    startMonth = int(startDate[5:7])
    endMonth = int(startDate[5:7])

    return JsonResponse({
        'graph': graph_json,
        'parameters': {
            'timeSlider': {
                'startYear': startYear,
                'startMonth': startMonth,
                'endYear': endYear,
                'endMonth': endMonth
            }
        }
    })

def chordDiagram(request):
    import numpy as np
    
    from chord import Chord

    df_enron = filterDataByTime(request ,pd.read_csv(request.FILES['csv_data']))
    names = ['Managing Director', 'In House Lawyer', 'Vice President', 'Employee', 'Unknown', 'Manager', 'Director', 'Trader', 'CEO', 'President']

    df_chord = df_enron.groupby(['fromJobtitle', 'toJobtitle'])['date'].count()
    df_chord = df_chord.unstack().fillna(0).astype(int)
    df_chord = df_chord.reindex(names)
    df_chord = df_chord[names]

    matrix = df_chord.values.tolist()

    print(Chord(matrix, names, wrap_labels=False))

    return HttpResponse(Chord(matrix, names, wrap_labels=False).to_html())

def individualInfo(request):

    import matplotlib.pyplot as plt

    plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
    plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

    # reveal a hint only while holding the mouse down
    from IPython.display import HTML
    HTML("<style>.h,.c{display:none}.t{color:#296eaa}.t:active+.h{display:block;}</style>")

    # hide FutureWarnings, which may show for Seaborn calls in most recent Anaconda
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    df_enron = pd.read_csv(request.FILES['csv_data'])
    Person_ID_1, ID_mail, job_title, mails_send, mean_sentiment_send, min_sentiment_send, max_sentiment_send, mails_received, mean_sentiment_received, min_sentiment_received, max_sentiment_received, array_mails_sent, array_mails_received = getIndividualInfoInner(df_enron, int(request.POST['person_id']))
    
    df_enron_tf = filterDataByTime(request,df_enron)
    Person_ID_1_tf, ID_mail_tf, job_title_tf, mails_send_tf, mean_sentiment_send_tf, min_sentiment_send_tf, max_sentiment_send_tf, mails_received_tf, mean_sentiment_received_tf, min_sentiment_received_tf, max_sentiment_received_tf, array_mails_sent_tf, array_mails_received_tf = getIndividualInfoInner(df_enron_tf, int(request.POST['person_id']))

    #Person_ID_1, ID_mail, job_title, mails_send, mean_sentiment_send, min_sentiment_send, max_sentiment_send, mails_received, mean_sentiment_received, min_sentiment_received, max_sentiment_received
    return JsonResponse({
        'meta': {
            'person_id': str(Person_ID_1),
            'mail_address': str(ID_mail),
            'job_title': str(job_title),
        },
        'all_time': {
            'mails_sent': str(mails_send),
            'min_sentiment_sent': str(min_sentiment_send),
            'mean_sentiment_sent': str(mean_sentiment_send),
            'max_sentiment_sent': str(max_sentiment_send),
            'array_mails_sent': array_mails_sent,
            'mails_received': str(mails_received),
            'min_sentiment_received': str(min_sentiment_received),
            'mean_sentiment_received': str(mean_sentiment_received),
            'max_sentiment_received': str(max_sentiment_received),
            'array_mails_received': array_mails_received,
        },
        'time_filtered': {
            'mails_sent': str(mails_send_tf),
            'min_sentiment_sent': str(min_sentiment_send_tf),
            'mean_sentiment_sent': str(mean_sentiment_send_tf),
            'max_sentiment_sent': str(max_sentiment_send_tf),
            'array_mails_sent': array_mails_sent_tf,
            'mails_received': str(mails_received_tf),
            'min_sentiment_received': str(min_sentiment_received_tf),
            'mean_sentiment_received': str(mean_sentiment_received_tf),
            'max_sentiment_received': str(max_sentiment_received_tf),
            'array_mails_received': array_mails_received_tf,
        }
    })

def getIndividualInfoInner(df_enron, person_id):
    Person_ID_1 = person_id
    person_send = df_enron['fromId'] == Person_ID_1
    person_received = df_enron['toId'] == Person_ID_1
    df_1 = df_enron[person_send]
    df_2 = df_1[['fromEmail']]
    df_3 = df_2.describe()
    ID_mail = df_3['fromEmail']['top']
    df_describe_person = df_1[['fromJobtitle']].describe()
    job_title = df_describe_person['fromJobtitle']['top']
    mails_send = df_1['sentiment'].count()
    mean_sentiment_send = df_1['sentiment'].mean()
    min_sentiment_send = df_1['sentiment'].min()
    max_sentiment_send = df_1['sentiment'].max()
    df_received = df_enron[person_received]
    mails_received = df_received['sentiment'].count()
    mean_sentiment_received = df_received['sentiment'].mean()
    min_sentiment_received = df_received['sentiment'].min()
    max_sentiment_received = df_received['sentiment'].max()
    emails_sent = 'none'
    try:
        df_emails_sent_1 = df_1.groupby('toId').describe()
        df_emails_sent_2 = df_emails_sent_1['fromId']
        emails_sent = df_emails_sent_2[['count']].to_json()
    except:
        pass
    emails_received = 'none'
    try:
        emails_received_1 = df_received.groupby('fromId').describe()
        emails_received_2 = emails_received_1['toId']
        emails_received = emails_received_2[['count']].to_json()
    except:
        pass
    return Person_ID_1, ID_mail, job_title, mails_send, mean_sentiment_send, min_sentiment_send, max_sentiment_send, mails_received, mean_sentiment_received, min_sentiment_received, max_sentiment_received, emails_sent, emails_received
