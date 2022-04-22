from arcgis.geocoding import geocode
from arcgis.gis import GIS
import csv

API_KEY = "AAPKe8b6e264681244eeb1f1bf14ef5141baGa9LTw55OAhHSw8-GYTEoxz5e-y5T2OO7ykh_eqFJEPRODndP5Iwx6gIkMj3xDfm"
MENTAL_HEALTH_DATABASE = "/Users/nicholasbarrow/GitHub/dc-mental-health-centers/dc-mental-health-centers-database.csv"
gis = GIS(api_key=API_KEY)


class Location:
    def __init__(self, name: str, address: str, youth: str):
        self.name = name
        self.address = address
        self.youth = youth
        self.x = None
        self.y = None

    @classmethod
    def from_unformatted_string(cls, name, address, youth):
        t = address.replace("\n", ",")
        return cls(name, t, youth)

    def __str__(self):
        return f"{self.name} @ {self.address}"


def main():
    locations = []
    with open(MENTAL_HEALTH_DATABASE, "r") as databasefile:
        items = csv.reader(databasefile)
        for index, row in enumerate(items):
            if index != 0:
                locations.append(Location.from_unformatted_string(row[0], row[2], row[4]))
            else:
                print(row)
    for location in locations:
        # print(location)
        results = geocode(location.address)
        if len(results) != 1:
            # print(f"{len(results)} - {location}")
            keep = results[0]
            for result in results[1:]:
                # print(result)
                if keep['score'] < result['score']:
                    keep = result
                    print("swapped")
            location.x = keep['location']['x']
            location.y = keep['location']['y']
        else:
            location.x = results[0]['location']['x']
            location.y = results[0]['location']['y']
    with open("output.csv", "w") as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(["Name", "Address", "Serves Children/Youth", "x", "y"])
        for location in locations:
            assert location.x is not None and location.y is not None and location.name is not None and location.address is not None and location.youth is not None
            writer.writerow([location.name, location.address, location.youth, location.x, location.y])

if __name__ == "__main__":
    main()
