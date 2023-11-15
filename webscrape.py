import csv
import requests
import json
from datetime import date, timedelta, datetime

rates = []


with open("HotelDetails.csv", 'r') as file:
  csvreader = csv.reader(file)
  for rows in csvreader:
    #if checkin date is not available the code would change it to today's date 
    if rows[1] == "":
        rows[1] = date.today()
    #if checkout date is not available the code would change it to checkin date plus one day    
    if rows[2] == "":
        checkinDate = datetime.strptime(rows[1], "%Y-%m-%d")
        rows[2] =checkinDate + timedelta(days=1)
        rows[2] = rows[2].date()
    #found a frontend api will all the desired information manipulating the same
    feCall = f"https://www.qantas.com/hotels/api/ui/properties/{rows[0]}/availability?checkIn={rows[1]}&checkOut={rows[2]}&adults=2&children=0&infants=0&payWith=cash"

    headers = {
        'Referer': feCall
    }
    response = requests.get(feCall,headers=headers)
    if response.status_code == 200:
       data = response.json()
       for i in range(len(data['roomTypes'])):
         for x in range(len(data['roomTypes'][i]['offers'])):
           print("Room Name : " + (data['roomTypes'][i]['name']))
           rates.append("Room Name : " + (data['roomTypes'][i]['name']))
           print("Number of Guests : " + str((data['roomTypes'][i]['maxOccupantCount'])))
           rates.append("Number of Guests : " + str((data['roomTypes'][i]['maxOccupantCount'])))
           print("Rate Name : " +data['roomTypes'][i]['offers'][x]['name'])
           rates.append("Rate Name : " +data['roomTypes'][i]['offers'][x]['name'])
           print("Cancellation Policy : " +data['roomTypes'][i]['offers'][x]['cancellationPolicy']['description'])
           rates.append("Cancellation Policy : " +data['roomTypes'][i]['offers'][x]['cancellationPolicy']['description'])
           print("Price : " +data['roomTypes'][i]['offers'][x]['charges']['total']['amount'])
           rates.append("Price : " +data['roomTypes'][i]['offers'][x]['charges']['total']['amount'])
           if data['roomTypes'][i]['offers'][x]['charges']['total']['amount']:
             print("Top Deal : " + str(True))
             rates.append("Top Deal : " + str(True))
           else:
             print("Top Deal : " + str(False))  
             rates.append("Top Deal : " + str(False))
           print("Price : " +data['roomTypes'][i]['offers'][x]['charges']['total']['currency'])
           rates.append("Price : " +data['roomTypes'][i]['offers'][x]['charges']['total']['currency'])
           print("\n")

    else:
      print("Data Not Available")

print(json.dumps(rates))