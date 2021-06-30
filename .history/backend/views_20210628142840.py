
########Backend Utility Libs#####
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

import django.http
import json
################################

########Data Science and Graph libs######
import pandas as pd
import networkx
import matplotlib.pyplot as plt
import numpy as np


########Normal Graph############
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Category10
from bokeh.transform import linear_cmap
from bokeh.embed import json_item


############Chord################
import numpy as np
    
from chord import Chord
########################################




############Filtering###############
def filterDataByTime(request, data):
    startDate = request.POST.get("start_date", '0000-00-00')
    endDate = request.POST.get("end_date", '9999-99-99')
    return data[ ((data["date"]>=startDate) & (data["date"] <= endDate)) ]

def filterDataByJobtitle(request, data):
    if not 'job_titles' in request.POST: return data

    fromMask = data["fromJobtitle"] == '___'
    toMask = data["toJobtitle"] == '___'

    for i in request.POST.get("job_titles").split(','):
        fromMask |= (data["fromJobtitle"] == i)
        toMask |= (data["toJobtitle"] == i)

    return data[(fromMask & toMask)]

def filterDataBySentiment(request,data):
    mask = data["sentiment"] == 10
    filterSelected = False
    if 'sentiment_negative' in request.POST:
        mask |= (data["sentiment"] <= -0.1)
        filterSelected = True
    if 'sentiment_neutral' in request.POST:
        mask |= ((data["sentiment"] >= -0.1) & (data["sentiment"] <= 0.1))
        filterSelected = True
    if 'sentiment_positive' in request.POST:
        mask |= (data["sentiment"] >= 0.1)
        filterSelected = True
    if (filterSelected):
        print(len(data))
        print(len(data[mask]))
        return data[mask]
    return data

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
    finalData = filterDataByJobtitle(request, finalData)
    finalData = filterDataBySentiment(request, finalData)
    #return filterDataByJobtitles(request, finalData) 
    return finalData

################################################################

#######Mean Sentiment##########
def getMeanSentiment(df):
    df[["sentiment"]].mean().values[0]

def index(request):
    return render(request, 'index.html')

def makeGraph(request, df_enron):
    G = networkx.from_pandas_edgelist(df_enron, 'fromId', 'toId', edge_attr=True)

    di = {'CEO':1,'Director':2,'Employee':3,'In House Lawyer':4,'Manager':5,'Managing Director':6,'President':7,'Trader':8,'Unknown':9,'Vice President':10}
    df_rejob = df_enron.replace({"fromJobtitle": di})
    df_attributes = df_enron[['fromId', 'fromJobtitle', 'fromEmail']].drop_duplicates()
    df_attributes.columns = ['fromId', 'job', 'fromEmail']
    df_attributesx = df_rejob[['fromId', 'fromJobtitle', 'fromEmail']].drop_duplicates()
    job = df_attributes.set_index('fromId').to_dict('i')
    jobx = df_attributesx.set_index('fromId').to_dict('i')
    fromEmail = df_attributes.set_index('fromEmail').to_dict('i')
    networkx.set_node_attributes(G, job)
    networkx.set_node_attributes(G, jobx)
    networkx.set_node_attributes(G, fromEmail)
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
        ("Email", "@fromEmail"),
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
    # import holoviews as hv
    # from holoviews import opts, dim
    # import networkx as nx
    # import dask.dataframe as dd
    # from holoviews.selection import link_selections
    # from holoviews.operation.datashader import (
    #     datashade, dynspread, directly_connect_edges, bundle_graph, stack
    # )
    # from holoviews.element.graphs import layout_nodes
    # from datashader.layout import random_layout
    # from colorcet import fire
    # import pandas as pd
    # import networkx
    # import matplotlib.pyplot as plt
    # import numpy as np
    # from bokeh.plotting import figure
    # from bokeh.resources import CDN
    # from bokeh.embed import file_html

    # hv.extension('bokeh')
    # df_chord = df_enron.sort_values('fromJobtitle')
    # df_chord['index'] = df_chord.index
    # df_links = df_chord.groupby(['fromId', 'toId']).count()
    # df_links = df_links.reset_index()[['fromId','toId', 'date']]
    # df_links.columns = ['source', 'target', 'value']
    # x = df_chord[['fromId', 'fromJobtitle']].drop_duplicates()
    # x.columns = ['source', 'fromJobtitle']

    # df_links = pd.merge(df_links, x, on="source")
    # df_nodes = df_chord[['fromId','fromEmail', 'fromJobtitle']].drop_duplicates().reset_index(drop=True)
    # df_nodes.columns = ['index', 'name', 'group']
    # df_nodes.sort_values('name')
    # y = df_chord[['fromId', 'toId']].drop_duplicates().groupby(['fromId']).count().reset_index()
    # y.columns = ['index', 'sizeOut']
    # y['sizeIn'] = df_chord[['fromId', 'toId']].drop_duplicates().groupby(['toId']).count().reset_index()[['fromId']]
    # y['size'] = y['sizeIn'] + y['sizeOut']
    # df_nodes = pd.merge(df_nodes, y, on='index')
    # df_nodes['size2'] = df_nodes['size']/3+8
    # from bokeh.models import Circle

    # nodes = hv.Dataset(df_nodes, 'index')
    # edge_df = df_links

    # eb_graph = hv.Graph((edge_df, nodes))

    # T_graph = layout_nodes(eb_graph, layout=nx.spring_layout)
    # #B_graph_3 = bundle_graph(T_graph)
    # from bokeh.models import HoverTool
    # TOOLTIPS = [
    #     ("Person ID", "@index"),
    #         ("people communicated with", "@size"),
    #         ("Jobtitle","@group"),
    # ]
    # hover = HoverTool(tooltips=TOOLTIPS)
    # graph_size = int(request.POST.get('graph_size', '720'))
    # #B_graph_3.options(node_color='group', cmap='Category20', node_size='size2', show_legend=True, tools=[hover],frame_width=graph_size, frame_height=graph_size)
    # T_graph.options(node_color='group', cmap='Category20', node_size='size2', show_legend=True, tools=[hover],frame_width=graph_size, frame_height=graph_size)

    # # # json_graph = json_item(B_graph_3)

    # # json_graph = json_item(T_graph)
    # # item_text = json.dumps(json_graph)

    # # return item_text

    # renderer = hv.renderer('bokeh')
    # plot = renderer.get_plot(T_graph)

    # return file_html(plot, CDN, "Plot")

def fullSizeGraph(request):
    
    graph_json = makeGraph(request, filter(request,pd.read_csv(request.FILES['csv_data'])))
    # return django.http.JsonResponse(graph_json, safe=False)
    return JsonResponse({
        'graph': graph_json
    })

def initialFullSizeGraph(request):
    
    df_dataset = pd.read_csv(request.FILES['csv_data'])
    
    startDate = df_dataset["date"].min()
    endDate = df_dataset["date"].max()

    startYear = int(startDate[:4])
    endYear = int(endDate[:4])

    startMonth = int(startDate[5:7])
    endMonth = int(startDate[5:7])

    jobTitles = df_dataset.fromJobtitle.unique().tolist()

    graph_json = makeGraph(request, df_dataset)

    return JsonResponse({
        'graph': graph_json,
        'parameters': {
            'timeSlider': {
                'startYear': startYear,
                'startMonth': startMonth,
                'endYear': endYear,
                'endMonth': endMonth
            },
            'jobTitles': jobTitles
        }
    })

def chordDiagram(person_id, df_enron):
    import holoviews as hv
    from holoviews import opts
    from bokeh.resources import CDN
    from bokeh.embed import file_html

    hv.extension('bokeh')

    df_chord = df_enron.sort_values('fromJobtitle')
    df_chord['index'] = df_chord.index

    df_links = df_chord.groupby(['fromId', 'toId']).agg({'date':'count', 'sentiment':'mean'})
    df_links = df_links.reset_index()[['fromId','toId', 'date', 'sentiment']]
    df_links.columns = ['source', 'target', 'value', 'sentiment']

    x = df_chord[['fromId', 'fromJobtitle']].drop_duplicates()
    x.columns = ['source', 'fromJobtitle']

    df_links = pd.merge(df_links, x, on="source")
    df_links.drop_duplicates(subset='source')

    df_nodes = df_chord[['fromId','fromEmail', 'fromJobtitle']].drop_duplicates().reset_index(drop=True)
    df_nodes.columns = ['index', 'name', 'group']
    df_nodes.sort_values('name')
    y = df_chord[['fromId', 'toId']].drop_duplicates().groupby(['fromId']).count().reset_index()
    y.columns = ['index', 'size']
    df_nodes = pd.merge(df_nodes, y, on='index')
    df_nodes['size'] = df_nodes['size']/3+8

    nodes = hv.Dataset(df_nodes, 'index')
    edge_df = df_links

    import seaborn as sns  # also improves the look of plots
    sns.set()  # set Seaborn defaults

    chord = hv.Chord((df_links, nodes)).select(value=(5, None))
    chord.opts(
        opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color='sentiment', 
                labels='name', node_color='group', edge_alpha=0.8, edge_line_width=1.5))

    final_chord = chord.select(index=person_id)

    plot = hv.render(final_chord, backend='bokeh')
    item_text = json.dumps(json_item(plot))
    return item_text

    # renderer = hv.renderer('bokeh')
    # plot = renderer.get_plot(final_chord).state
    # return file_html(plot, CDN, "Plot")

def individualInfo(request):

    # import matplotlib.pyplot as plt

    # plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
    # plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

    # # reveal a hint only while holding the mouse down
    # from IPython.display import HTML
    # HTML("<style>.h,.c{display:none}.t{color:#296eaa}.t:active+.h{display:block;}</style>")

    # # hide FutureWarnings, which may show for Seaborn calls in most recent Anaconda
    # import warnings
    # warnings.filterwarnings("ignore", category=FutureWarning)

    person_id = int(request.POST['person_id'])

    df_enron = pd.read_csv(request.FILES['csv_data'])
    Person_ID_1, ID_mail, job_title, mails_send, mean_sentiment_send, min_sentiment_send, max_sentiment_send, mails_received, mean_sentiment_received, min_sentiment_received, max_sentiment_received, array_mails_sent, array_mails_received, p_most_received_emails, most_received_emails_nr, p_most_sent_emails, most_sent_emails_nr = getIndividualInfoInner(df_enron, person_id)
    
    df_enron_tf = filter(request,df_enron)
    Person_ID_1_tf, ID_mail_tf, job_title_tf, mails_send_tf, mean_sentiment_send_tf, min_sentiment_send_tf, max_sentiment_send_tf, mails_received_tf, mean_sentiment_received_tf, min_sentiment_received_tf, max_sentiment_received_tf, array_mails_sent_tf, array_mails_received_tf, p_most_received_emails_tf, most_received_emails_nr_tf, p_most_sent_emails_tf, most_sent_emails_nr_tf = getIndividualInfoInner(df_enron_tf, person_id)

    chord = chordDiagram(person_id, df_enron)

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
            'most_emails_received_from' : str(p_most_received_emails),
            'number_received' : str(most_received_emails_nr),
            'most_emails_sent_to' : str(p_most_sent_emails),
            'number_sent' : str(most_sent_emails_nr),
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
            'most_emails_received_from' : str(p_most_received_emails_tf),
            'number_received' : str(most_received_emails_nr_tf),
            'most_emails_sent_to' : str(p_most_sent_emails_tf),
            'number_sent' : str(most_sent_emails_nr_tf),
            'array_mails_received': array_mails_received_tf,
        },
        'chord': chord
    })

def getIndividualInfoInner(df_enron, person_id):
    person_send = df_enron['fromId'] == person_id
    person_received = df_enron['toId'] == person_id
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


    

    df_person = df_enron[person_send | person_received]
    person = df_person.groupby(["fromId"])[["fromEmail"]].count().sort_values(by = "fromEmail", ascending = False).iloc[[0]]

    person_with_most_received_emails = person.index.values[0]
    nr_received_emails = person.values[0][0]

    person = df_person.groupby(["toId"])[["toEmail"]].count().sort_values(by = "toEmail", ascending = False).iloc[[0]]

    person_with_most_sent_emails =  person.index.values[0]
    nr_sent_emails = person.values[0][0]

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
    return person_id, ID_mail, job_title, mails_send, mean_sentiment_send, min_sentiment_send, max_sentiment_send, mails_received, mean_sentiment_received, min_sentiment_received, max_sentiment_received, emails_sent, emails_received, person_with_most_received_emails, nr_received_emails, person_with_most_sent_emails, nr_sent_emails
    #from bokeh.io import output_notebook, show, save
