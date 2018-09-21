# coding=utf-8
import ConfigParser, os
from google.cloud import datastore
from datetime import datetime
from pytz import timezone


class ConnectGCP:
    key = None
    project = None
    weatherkind = None
    datastoreClient = None
    requireData = ["id", "temperature", "humidity"]

    def __init__(self, ini):
        print ini
        config = ConfigParser.SafeConfigParser()
        config.read(ini)
        self.key = os.path.dirname(__file__) + '/' + config.get("GCP","keyfile")
        self.weatherkind = config.get("GCP", "kind")
        self.project = config.get("GCP", "project")

    def connectDS(self):
        self.datastoreClient = datastore.Client.from_service_account_json(
            self.key,
            project=self.project)

    def GetWeatherByID(self, device_id):
        query = self.datastoreClient.query(kind=self.weatherkind)
        query.add_filter("device_id", "=", device_id)
        return query.fetch()

    def postData(self, data):

        # validation
        print "aho"
        print type(data)
        for key in self.requireData:
            try:
                if data[key] is None:
                    return (False, "{},{}".format(key, data[key]))
            except:
                print "ERROR: {}".format(key)
                return False

        # id -> device_id
        data["device_id"] = data.pop("id")

        now = datetime.now(timezone('UTC'))

        # keyの作成
        ekey = datastore.key.Key(
            "weatherData",
            "{}-{}".format(now.strftime('%s'), data["device_id"]),
             project=self.project
        )
        print ekey

        # entityの作成
        entity = datastore.entity.Entity(key=ekey)

        # タイムスタンプ追加
        entity["datetime"] = now

        # dataを追加
        entity.update(data)

        for k in entity.keys():
            print "{}:{}".format(k,entity[k])

        # GCPにPOST
        self.datastoreClient.put(entity)

        return True



    def dummy(self, str):
        return self.__JST2UTC(str)

    def __JST2UTC(self,date):
        d = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        jstd = timezone('Asia/Tokyo').localize(d)
        return jstd.astimezone(timezone('UTC'))
