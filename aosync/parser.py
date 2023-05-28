from aosync.models import Tag, Stream, Chart, Dashboard


def _tag_from_response(response):
    name = response['name']
    # Returns an empty list if 'values' doesn't exist
    values = response.get('values', [])
    grouped = response.get('grouped', None)
    dynamic = response.get('dynamic', None)
    return Tag(name=name, values=values, grouped=grouped, dynamic=dynamic)


def _stream_from_response(response):
    metric = response.get('metric')
    if response.get('tags') is None:
        tags = None
    else:
        tags = [_tag_from_response(tag) for tag in response.get('tags')]
    composite = response.get('composite')
    group_function = response.get('group_function', None)
    summary_function = response.get('summary_function', None)
    downsample_function = response.get('downsample_function', None)
    color = response.get('color', None)
    name = response.get('name', None)
    units_short = response.get('units_short', None)
    units_long = response.get('units_long', None)
    min = response.get('min', None)
    max = response.get('max', None)
    transform_function = response.get('transform_function', None)
    period = response.get('period', None)
    return Stream(
        metric=metric,
        tags=tags,
        composite=composite,
        group_function=group_function,
        summary_function=summary_function,
        downsample_function=downsample_function,
        color=color,
        name=name,
        units_short=units_short,
        units_long=units_long,
        min=min,
        max=max,
        transform_function=transform_function,
        period=period
    )


def _chart_from_response(response):
    name = response.get('name')
    type = response.get('type')
    chart_id = response.get('id')
    min = response.get('min', None)
    max = response.get('max', None)
    label = response.get('label', None)
    related_space = response.get('related_space', None)
    streams = [_stream_from_response(stream) for stream in response['streams']]
    return Chart(
        name=name,
        type=type,
        streams=streams,
        id=chart_id,
        min=min,
        max=max,
        label=label,
        related_space=related_space
    )


def map_to_dashboard(charts_data, dashboard_data) -> Dashboard:
    charts = [_chart_from_response(chart) for chart in charts_data]
    return Dashboard(
        name=dashboard_data['name'],
        charts=charts,
        id=dashboard_data['id'],
    )
