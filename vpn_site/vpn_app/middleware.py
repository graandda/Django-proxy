from .models import Site, TrafficStatistic


class DataSizeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if str(request.path).split("/")[1] == "proxy":

            # Вимірюємо обсяг даних, переданих у тілі запиту
            request_data_size = len(request.body) if request.body else 0
            response = self.get_response(request)
            # Вимірюємо обсяг даних, переданих у тілі відповіді
            response_data_size = len(response.content) if response.content else 0

            site = Site.objects.get(
                user=request.user, name=str(request.path).split("/")[2]
            )

            user_statistics, created = TrafficStatistic.objects.get_or_create(
                user=request.user, site=site
            )
            if created:
                user_statistics.data_uploaded += response_data_size
                user_statistics.data_downloaded += request_data_size

            else:
                user_statistics.data_uploaded += response_data_size
                user_statistics.data_downloaded += request_data_size

            user_statistics.page_views += 1
            user_statistics.save()

        return response
