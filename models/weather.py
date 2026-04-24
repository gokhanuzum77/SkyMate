class Weather:
    def __init__(self, city, temp, desc, humidity, wind):
        self.__city = city
        self.__temp = temp
        self.__desc = desc
        self.__humidity = humidity
        self.__wind = wind

    def get_city(self):
        return self.__city

    def get_temp(self):
        return self.__temp

    def get_desc(self):
        return self.__desc

    def get_humidity(self):
        return self.__humidity

    def get_wind(self):
        return self.__wind