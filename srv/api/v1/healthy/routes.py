from aiohttp.web import Application

from srv.api.v1.healthy.views import LivenessView, ReadinessView


def create_routes(app: Application, path_prefix: str) -> None:
    app.router.add_view(f"{path_prefix}/liveness", LivenessView)
    app.router.add_view(f"{path_prefix}/readiness", ReadinessView)
