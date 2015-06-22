from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

from models import GradedFlowTarget, GradedFlowTargetElement

from waterkit import rasterflow

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import figure

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
    fig = Figure()
    ax = fig.add_subplot(111)
    rasterflow.raster_plot(data, attribute, "Flow Gap Plot", ax=ax)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    
