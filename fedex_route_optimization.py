import requests
import tkinter as tk
from tkinter import messagebox

TOMTOM_API_KEY = 'your_tomtom_api_key'
GOOGLE_MAPS_API_KEY = 'your_google_maps_api_key'
AQICN_API_KEY = 'your_aqicn_api_key'

def get_traffic_data(start_lat, start_lon, end_lat, end_lon):
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json?key={TOMTOM_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['routes'][0]['summary']['trafficTimeInSeconds']

def get_route_data(start_lat, start_lon, end_lat, end_lon):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_lat},{start_lon}&destination={end_lat},{end_lon}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['routes'][0]['legs'][0]['duration']['value'], data['routes'][0]['legs'][0]['distance']['value']

def get_air_quality_data(city):
    url = f"http://api.waqi.info/feed/{city}/?token={AQICN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['data']['aqi']

def estimate_emissions(vehicle_type, distance, air_quality):
    emission_factor = 0.12 if vehicle_type == "gasoline" else 0.08  # in grams per km
    emissions = emission_factor * distance
    emissions *= (1 + (air_quality / 100))
    return emissions

def calculate_optimal_route(vehicle_type, start_lat, start_lon, end_lat, end_lon, city):
    traffic_time = get_traffic_data(start_lat, start_lon, end_lat, end_lon)
    
    route_duration, route_distance = get_route_data(start_lat, start_lon, end_lat, end_lon)
    
    air_quality = get_air_quality_data(city)
    
    emissions = estimate_emissions(vehicle_type, route_distance / 1000, air_quality)  # convert distance to km
    
    return route_duration, route_distance, emissions, traffic_time

class RouteOptimizationApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Dynamic Route Optimization and Emission Reduction")
        
        self.create_widgets()
    
    def create_widgets(self):
        self.vehicle_type_label = tk.Label(self.root, text="Vehicle Type (gasoline/electric):")
        self.vehicle_type_label.grid(row=0, column=0)
        
        self.vehicle_type_entry = tk.Entry(self.root)
        self.vehicle_type_entry.grid(row=0, column=1)
        
        self.start_lat_label = tk.Label(self.root, text="Start Latitude:")
        self.start_lat_label.grid(row=1, column=0)
        
        self.start_lat_entry = tk.Entry(self.root)
        self.start_lat_entry.grid(row=1, column=1)
        
        self.start_lon_label = tk.Label(self.root, text="Start Longitude:")
        self.start_lon_label.grid(row=2, column=0)
        
        self.start_lon_entry = tk.Entry(self.root)
        self.start_lon_entry.grid(row=2, column=1)
        
        self.end_lat_label = tk.Label(self.root, text="End Latitude:")
        self.end_lat_label.grid(row=3, column=0)
        
        self.end_lat_entry = tk.Entry(self.root)
        self.end_lat_entry.grid(row=3, column=1)
        
        self.end_lon_label = tk.Label(self.root, text="End Longitude:")
        self.end_lon_label.grid(row=4, column=0)
        
        self.end_lon_entry = tk.Entry(self.root)
        self.end_lon_entry.grid(row=4, column=1)
        
        self.city_label = tk.Label(self.root, text="City (for air quality):")
        self.city_label.grid(row=5, column=0)
        
        self.city_entry = tk.Entry(self.root)
        self.city_entry.grid(row=5, column=1)
        
        self.calculate_button = tk.Button(self.root, text="Calculate Route", command=self.calculate_route)
        self.calculate_button.grid(row=6, column=0, columnspan=2)
        
        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=7, column=0, columnspan=2)
    
    def calculate_route(self):
        vehicle_type = self.vehicle_type_entry.get()
        start_lat = float(self.start_lat_entry.get())
        start_lon = float(self.start_lon_entry.get())
        end_lat = float(self.end_lat_entry.get())
        end_lon = float(self.end_lon_entry.get())
        city = self.city_entry.get()
        
        route_duration, route_distance, emissions, traffic_time = calculate_optimal_route(vehicle_type, start_lat, start_lon, end_lat, end_lon, city)
        
        self.result_label.config(text=f"Route Duration: {route_duration / 60:.2f} minutes\n"
                                     f"Route Distance: {route_distance / 1000:.2f} km\n"
                                     f"Emissions: {emissions:.2f} grams CO2\n"
                                     f"Traffic Time: {traffic_time / 60:.2f} minutes")

root = tk.Tk()
app = RouteOptimizationApp(root)
root.mainloop()
