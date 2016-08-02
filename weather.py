import RPi.GPIO as GPIO
import time
import urllib2, urllib, json
import os, sys

pins = [11, 12, 13, 15]

url = "http://api.wunderground.com/api/[api_key]/conditions/q/52.930788,5.026149.json"

def setup():
	GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output
		GPIO.output(pin, GPIO.HIGH) # Set all pins to high(+3.3V) to off led

def loop():
	while True:
            result = urllib2.urlopen(url).read()
            data = json.loads(result)

            for pin in pins:
                GPIO.output(pin, GPIO.HIGH)

  	    print data['current_observation']['icon']
	    #sys.stdout.write(data['current_observation']['icon'])
    	    #sys.stdout.flush()

	    rain 	= ["rain", "chanceflurries", "chancerain", "unknown"]
	    thunder 	= ["tstorms", "chancetstorms", "chancetstorms"]
	    cloudy	= ["cloudy", "fog", "hazy", "mostlycloudy"]
  	    sun 	= ["sunny", "clear", "mostlysunny", "partlycloudy", "partlysunny"]
	    snow 	= ["snow", "chancesnow", "chancesleet", "flurries", "sleet"]

            if data['current_observation']['icon'] in rain:
                GPIO.output(15, GPIO.LOW)

	    if data['current_observation']['icon'] in sun:
                GPIO.output(12, GPIO.LOW)

	    if data['current_observation']['icon'] in thunder:
                GPIO.output(11, GPIO.LOW)
                GPIO.output(12, GPIO.LOW)

	    if data['current_observation']['icon'] in cloudy:
                GPIO.output(15, GPIO.LOW)
                GPIO.output(13, GPIO.LOW)

	    if data['current_observation']['icon'] in snow:
                GPIO.output(13, GPIO.LOW)

	    time.sleep(300)

def destroy():
	for pin in pins:
		GPIO.output(pin, GPIO.HIGH)    # turn off all leds
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
            loop()
	except:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		loop()
