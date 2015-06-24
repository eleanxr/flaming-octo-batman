from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from models import GradedFlowTarget, GradedFlowTargetElement

from waterkit import rasterflow

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors

import pandas as pd

def index(request):
    flow_targets = GradedFlowTarget.objects.all()
    return render(request, 'flowviz/index.django.html', {'flow_targets': flow_targets})

def target(request, target_id):
    flow_target = get_object_or_404(GradedFlowTarget, pk=target_id)
    return render(request, 'flowviz/targetview.django.html', {'flow_target': flow_target})

def dynamic_raster(request, target_id, attribute):
    data = __read_data(target_id)
    
    # Get visualization parameters
    cmap = request.GET.get('cmap', None)
    title = request.GET.get('title', None)
    zero = request.GET.get('zero', 'False')
    logscale = request.GET.get('logscale', 'False')
    
    zero = zero == "True"
    logscale = logscale == "True"
    
    plt.style.use('ggplot')
    fig = Figure()
    ax = fig.add_subplot(111)
    
    min_value = data[attribute].min()
    max_value = data[attribute].max()
    if cmap:
        colormap = cm.get_cmap(cmap)
        if zero:
            colormap = rasterflow.create_colormap(data, attribute, colormap, vmin=min_value, vmax=max_value)
            colormap.set_bad('black')
    else:
        colormap = None
    if logscale:
        norm = matplotlib.colors.LogNorm()
    else:
        norm = None
    
    rasterflow.raster_plot(data, attribute, title, show_colorbar=True, norm=norm,
                           colormap=colormap, vmin=min_value, vmax=max_value, fig=fig, ax=ax)
    return __plot_to_response(fig)    

def __new_figure():
    fig = Figure()
    ax = fig.add_subplot(111)
    return (fig, ax)

def __read_data(target_id):
    flow_target = get_object_or_404(GradedFlowTarget, pk=target_id)
    target_data = rasterflow.GradedFlowTarget()
    for element in flow_target.gradedflowtargetelement_set.all():
        fr = "%d-%d" % (element.from_month, element.from_day)
        to = "%d-%d" % (element.to_month, element.to_day)
        target_data.add((fr, to), float(element.target_value))
    data = rasterflow.read_data(
        flow_target.location.identifier,
        "1950-01-01", "2014-12-31",
        target_data)
    return data

def __plot_to_response(fig):
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def deficit_stats_plot(request, target_id):
    data = __read_data(target_id)
    
    deficit = data[data['e-flow-gap'] < 0]
    
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    deficit.boxplot(by='month', column='e-flow-gap', ax=ax)
    ax.set_title('Deficit Statistics')
    return __plot_to_response(fig)

def deficit_days_plot(request, target_id):
    data = __read_data(target_id)
    days_in_deficit = data[data['e-flow-gap'] < 0].groupby('month').count()['e-flow-gap']
    total_days = data.groupby('month').count()['e-flow-gap']
    join = pd.concat([days_in_deficit, total_days], axis = 1)
    join.columns = ['gap', 'total']
    join['pct'] = 100.0 * join['gap'] / join['total']
    ax = join['pct']
    
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    join[join['pct'] > 0.0]['pct'].plot(kind = 'bar', ax=ax)
    ax.set_title('Percent of days in deficit')
    return __plot_to_response(fig)

def right_plot(request, target_id):
    data = __read_data(target_id)
    averages = data.groupby('dayofyear').mean()
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    plotdata = averages[['flow', 'e-flow-target']]
    plotdata.columns = ['Average Daily Flow (cfs)', 'Water Right (cfs)']
    plotdata.plot(ax=ax)
    ax.set_xlabel("Month")
    rasterflow.label_months(ax)
    return __plot_to_response(fig)

    
