
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import timeForm
import django.http
import json

def filterDataByTime(data):
    form = timeForm(request.POST or None)
    if form.is_valid():
        startDate = form.cleaned_data.get("startDate")
        endDate = form.cleaned_data.get("endDate")

    return data[data[date]>startDate & ]
        



def index(request):
    return render(request, 'index.html')

def fullSizeGraph(request):
    import pandas as pd
    import networkx
    import matplotlib.pyplot as plt
    import numpy as np

    df_enron = filterDataByTime(pd.read_csv(request.FILES['csv_data']))

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

    plot = figure(tooltips = TOOLTIPS,
                tools="pan,zoom_in,wheel_zoom,save,reset,box_select,undo", active_scroll='wheel_zoom',
                x_range=Range1d(-20,20), y_range=Range1d(-20,20),  title='Enron Emails',
                plot_width=950, plot_height=950)
    plot.axis.visible = False

    N_graph = from_networkx(G, networkx.spring_layout, scale=100)

    N_graph.node_renderer.glyph = Circle(size=size_by_this_attribute,
                                        fill_color=linear_cmap(color_by_this_attribute, color_palette, 1, 10))

    N_graph.edge_renderer.glyph = MultiLine(line_alpha=10, line_width=1)

    plot.renderers.append(N_graph)

    item_text = json.dumps(json_item(plot))

    return django.http.JsonResponse(item_text, safe=False)

def chordDiagram(request):
    import numpy as np
    import pandas as pd
    from chord import Chord

    df_enron = filterDataByTime(pd.read_csv(request.FILES['csv_data']))
    names = ['Managing Director', 'In House Lawyer', 'Vice President', 'Employee', 'Unknown', 'Manager', 'Director', 'Trader', 'CEO', 'President']

    df_chord = df_enron.groupby(['fromJobtitle', 'toJobtitle'])['date'].count()
    df_chord = df_chord.unstack().fillna(0).astype(int)
    df_chord = df_chord.reindex(names)
    df_chord = df_chord[names]

    matrix = df_chord.values.tolist()

    print(Chord(matrix, names, wrap_labels=False))

    return HttpResponse(Chord(matrix, names, wrap_labels=False).to_html())
