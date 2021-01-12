import requests
import json
from constant import BROKER_SUMMARY_URL, PUBLIC_HOLIDAY_URL 
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR

class Utility:

    def convert_string_amount(amount_string):
        number = 0
        metric = 0
        multiplier = 1

        amount_splitted = amount_string.split(" ")

        if len(amount_splitted) > 0:
            number = float(amount_splitted[0].replace(",", ""))
        if len(amount_splitted) > 1:
            metric = amount_splitted[1]

        if metric == "M" :
            multiplier = float(1000000)
        if metric == "B" : 
            multiplier = float(1000000000)
        if metric == "T" : 
            multiplier = float(1000000000000)

        return number * multiplier

    def get_past_working_day(xday_ago, emiten_text):
        finish_process = False
        list_brokersum_url = {}
        gap_day = 1
        processed_day = 0
        current_date = datetime.now()

        #get national holiday of Indonesia
        public_holidays_api = requests.get(PUBLIC_HOLIDAY_URL)
        public_holidays = json.loads(public_holidays_api.text)

        while finish_process != True:
            date_processed = current_date - timedelta(days=gap_day)
            the_day = date_processed.strftime("%w")
            the_date = date_processed.strftime("%m/%d/%Y")
            if int(the_day) != 0 and int(the_day) != 6:
                date_string = date_processed.strftime("%Y%m%d")
                try:
                    public_holidays[date_string]
                except KeyError:
                    url_broker_summary = BROKER_SUMMARY_URL+emiten_text+'&start='+ the_date +'&end='+the_date+'&fd=all&board=RG'
                    list_brokersum_url[processed_day + 1] = url_broker_summary
                    processed_day +=1
                else:
                    print("sure, it was holyday.")

            if(processed_day == xday_ago):
                finish_process = True
                
            gap_day += 1
        
        return list_brokersum_url
