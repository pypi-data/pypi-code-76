import djclick as click
from django_apiview.models import ApiResponseTimeStats

@click.command()
def update_api_response_time_stats():
    info = ApiResponseTimeStats.update()
    print(info)

