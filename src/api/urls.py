from django.urls import path, include

from api.views.car_views.update_car_view import UpdateCarView
from api.views.cargo_views.create_cargo_view import CreateCargoView
from api.views.cargo_views.delete_cargo_view import DeleteCargoView
from api.views.cargo_views.get_cargo_by_id_view import GetCargoView
from api.views.cargo_views.get_cargos_view import GetCargosView
from api.views.cargo_views.update_cargo_view import UpdateCargoView

cargo_urlpatterns = [
    path('create/', CreateCargoView.as_view()),
    path('all', GetCargosView.as_view()),
    path('<int:cargo_id>/', GetCargoView.as_view()),
    path('update/<int:cargo_id>/', UpdateCargoView.as_view()),
    path('delete/<int:cargo_id>/', DeleteCargoView.as_view())
]

car_urlpatterns = [
    path('update/<int:car_id>/', UpdateCarView.as_view())
]

urlpatterns = [
    path('cargo/', include(cargo_urlpatterns)),
    path('car/', include(car_urlpatterns))
]