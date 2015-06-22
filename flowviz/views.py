from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from models import GradedFlowTarget, GradedFlowTargetElement

from waterkit import rasterflow

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def index(request):
    return render(request, 'flowviz/index.django.html')

def target(request, target_id):
    flow_target = get_object_or_404(GradedFlowTarget, pk=target_id)
    return render(request, 'flowviz/targetview.django.html', {'flow_target': flow_target})

def dynamic_raster(request, target_id, attribute):
    flow_target = get_object_or_404(GradedFlowTarget, pk=target_id)
    target_data = rasterflow.GradedFlowTarget()
    for element in flow_target.gradedflowtargetelement_set.all():
        fr = "%d-%d" % (element.from_month, element.from_day)
        to = "%d-%d" % (element.to_month, element.to_day)
        target_data.add((fr, to), element.target_value)
    data = rasterflow.read_data(
        flow_target.location.identifier,
        "1950-01-01", "2014-12-31",
        target_data)
    
    plt.style.use('ggplot')
    fig = Figure()
    ax = fig.add_subplot(111)
    base_colormap = cm.get_cmap('bwr_r')
    min_value = data[attribute].min()
    max_value = data[attribute].max()
    # If the data has negative values, only show their relative sizes
    if min_value < 0:
        max_value = -min_value
    colormap = rasterflow.create_colormap(data, attribute, base_colormap, vmin=min_value, vmax=max_value)
    colormap.set_bad('black')
    rasterflow.raster_plot(data, attribute, "Instream flow gap", show_colorbar=True,
                           colormap=colormap, vmin=min_value, vmax=max_value, fig=fig, ax=ax)
    
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    
