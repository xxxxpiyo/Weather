import ConfigParser, os
from google.cloud import datastore
from datetime import datetime
from pytz import timezone


class ConnectGCP:
    key = None
    project = None
    weatherkind = None
    datastoreClient = None

    def __init__(self, ini):
        config = ConfigParser.SafeConfigParser()
        config.read(ini)
        self.key = os.path.dirname(__file__) + '/' + config.get("GCP","keyfile")
        self.weatherkind = config.get("GCP", "kind")
        self.project = config.get("GCP", "project")

    def connectDS(self):
        self.datastoreClient = datastore.Client.from_service_account_json(self.key)

    def GetWeatherByID(self, device_id):
        query = client.query(kind=self.kind)
        query.add_filter("device_id", "=", device_id)
        return query.fetch()

    def postData(self, data):
        entity = datastore.entity.Entity()

    def dummy(self, str):

    def __JST2UTC(self,date):
        d = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        jstd = timezone('Asia/Tokyo').localize(d)
        return jstd.astimezone(timezone('UTC'))
