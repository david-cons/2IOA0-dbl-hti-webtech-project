
from django.shortcuts import render
# from django.http import JsonResponse
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def baseData(request):
    import pandas as pd
    import networkx
    from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
    from bokeh.plotting import figure
    from bokeh.palettes import Reds8
    from bokeh.io import output_notebook, show, save
    from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
    from bokeh.plotting import figure
    from bokeh.models.graphs import from_networkx
    from bokeh.transform import linear_cmap
    from bokeh.embed import file_html
    from bokeh.resources import CDN

    df_enron = pd.read_csv(request.FILES['csv_data'])

    G = networkx.from_pandas_edgelist(df_enron, 'fromEmail', 'toEmail', edge_attr=True)

    TOOLTIPS = [("email", "@index")]
    plot = figure(tooltips = TOOLTIPS,
                tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                x_range=Range1d(-10, 10), y_range=Range1d(-10, 10), title='Email')


    #network_graph = from_networkx(G2, networkx.spring_layout, scale=50, center=(0, 0))

    #Set node size and color
    #network_graph.node_renderer.glyph = Circle(size=10, fill_color='red')

    #Set edge opacity and width
    #network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

    #Add network graph to the plot
    #plot.renderers.append(network_graph)

    degrees = dict(networkx.degree(G))
    adjusted_node_size = dict([(node, (degree + 5) - ((degree + 5)*0.3) ) for node, degree in networkx.degree(G)])
    networkx.set_node_attributes(G, name='degree', values=degrees)
    networkx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'adjusted_node_size'

    color_palette = Reds8

    networkx.set_node_attributes(G, name='degree', values=degrees)

    TOOLTIPS = [
        ("Email address", "@index"),
            ("sent email address", "@degree"),
            ("Jobtitle","@job"),
    ]

    plot = figure(tooltips = TOOLTIPS,
                tools="pan,zoom_in,wheel_zoom,save,reset,box_select,undo", active_scroll='wheel_zoom',
                x_range=Range1d(-20,20), y_range=Range1d(-20,20),  title='Email')

    N_graph = from_networkx(G, networkx.spring_layout, scale=100)

    minimum_value_color = min(N_graph.node_renderer.data_source.data[color_by_this_attribute])
    maximum_value_color = max(N_graph.node_renderer.data_source.data[color_by_this_attribute])
    N_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=linear_cmap(color_by_this_attribute, color_palette, maximum_value_color,minimum_value_color))


    N_graph.edge_renderer.glyph = MultiLine(line_alpha=10, line_width=1)

    plot.renderers.append(N_graph)

    html = file_html(plot, CDN, "Base Data Plot")

    return HttpResponse(html)
