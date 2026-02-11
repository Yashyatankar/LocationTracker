import requests
import folium
import webbrowser
import os

def track_ip(ip_address=""):
    try:
        # Use ip-api.com (Free, no key required for basic use)
        # If ip_address is empty, it tracks the machine running the script
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            city = data['city']
            region = data['regionName']
            country = data['country']
            isp = data['isp']

            print(f"\n[+] IP Tracked: {data['query']}")
            print(f"[+] Location: {city}, {region}, {country}")
            print(f"[+] ISP: {isp}")
            print(f"[+] Coordinates: {lat}, {lon}")

            # Create Map UI
            # zoom_start=12 provides a good city-level view
            my_map = folium.Map(location=[lat, lon], zoom_start=12)
            
            # Add a Marker
            folium.Marker(
                [lat, lon], 
                popup=f"IP: {data['query']}\nLocation: {city}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(my_map)

            # Add a circle to show the approximate area (IPs aren't 100% exact)
            folium.Circle(
                radius=500,
                location=[lat, lon],
                color='crimson',
                fill=True,
            ).add_to(my_map)

            # Save and Open
            file_name = "ip_tracker_result.html"
            my_map.save(file_name)
            webbrowser.open('file://' + os.path.realpath(file_name))
            print(f"\n[!] Success: Map saved as {file_name}")

        else:
            print(f"[-] Failed to track IP: {data.get('message')}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target_ip = input("Enter IP address to track (leave blank for your own IP): ")
    track_ip(target_ip)
    