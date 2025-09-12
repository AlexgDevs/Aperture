from fastapi import Request

def register_middlewares(app):
    @app.middleware("http")
    async def collected_metric_data(request: Request, call_next):
        short_path = request.url.path
        sep_path = short_path.split('/')
        response = await call_next(request)

        if len(sep_path) in [3, 4] and sep_path[1] == 'links':
            if len(sep_path) == 4 and sep_path[2] == 'f':
                short = sep_path[3]
                endpoint_type = "fast"
            elif len(sep_path) == 3:
                short = sep_path[2]
                endpoint_type = "standard"
            else:
                return response

            request_data = {
                'ip_address': request.client.host,
                'user_agent': request.headers.get('user-agent', ''),
                'referer': request.headers.get('referer'),
                'accept_language': request.headers.get('accept-language', ''),
            }

            process_meta_collection.delay(
                short,
                endpoint_type,
                request_data
            )

        return response

from celery_tasks import process_meta_collection
