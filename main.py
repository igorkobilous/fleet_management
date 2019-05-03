from app import app

from fleet.resourses import api as fleet_api
from user.resourses import api as user_api
from vehicle.resourses import api as vehicle_api


if __name__ == '__main__':
    app.run()
