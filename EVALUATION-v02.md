# Test of a Heltec HT-CT62 / TI BQ25185 based Meshtastic node

## Case

![Meshtastic Node](./pictures/evaluation_case.jpg "The setup")


Lessons learned: 

  - Use 5-6mm spacers between the solar panel and the box. It indirectly can act as a sunshield. As solar panels are mostly black they heat up a lot and so shouldn't be directly attached to it.
  - White or silver spray reduces the temperature even more. Bonus if it's a highly reflective spray.
  - Gore venting plugs are very expensive but useful to control the humidity. Not overly  critical as long it's only normal water - but salty air like close to the ocean kills electronics. EDIT:
  - Alternative to Gore venting plugs: you can use syringe filters! They are cheap (100pcs@20€ at Aliexpress) with 0.8um pores .
  - Never use any hot glue. I switched to polymer adhesives used for boats and pools. A slight residual elasticity is desirable as it prevents breakage due to cable movement.



## Electronics

![Meshtastic Integration](./pictures/evaluation_integration.jpg)

Lessons learned:

 - Voltage dividers with 1M:1M and a 100nF puffer C works perfectly fine. The power drain is below the battery self discharge level and the ESP32 ADC is able to sample the voltage without getting too much noise.

 - The crappy ESP32 ADC isn't super precise. Known issue.

 - For panels up to ~6V the TI BQ25185 seems to be the right decision
   - It will get very hot at higher voltage levels because of its linear design. That inefficient and also bad for low temperature soldering paste.  
   - The end-of-charge voltage can be reduced in several steps to extend the battery life
   - Power path'ing switches the battery off if sunlight is enough to power the device. It's also able to mix both sources
   - Pseudo MPPT (VINDPM) always gets us the maximum amount of current out of the solar panel

- Don't use CR123A batteries. They are non-standard for 3.7V LiPos and there are a lot of fakes around. The missing market makes them very expensive.
   - Go for battery size 18650 or even 21700

- The ESP32C3 can be thamed in terms of current consumption. But let's be honest: it's not a Nordic or STM32U0.
  - Stay in light sleep as much as possible (theoretically ~600-800uA) and wake up by interrupts
  - Avoid BLE or Wifi at all costs


 ## Measurements

For a real world test I setup following hardware configuration:

 - ISET = 300Ohm: Solar current of 1A 
 - ILM = 100kOhm: Maximum charging voltage 4.1V@1100mA
 - Noname ~800mAh 3.7V CR123A LiPo
 - 6V 290mAh solar cell


 Meshtastic configuration:

  - Minimum Wake Interface: 1s (default: 10s)
  - Repeater Mode activated
  - BLE/Wifi disabled (configuration via UART)

 Syytem configuration:
  - ESP32C3 CPU speed reduced to 80MHz

The telemetry values are getting pulled from the device every 30 minutes and then getting stored into an InfluxDB which are getting visualized using Grafana.

Our Meshtastic network (Stuttgart/Germany) has around 22-50 users.

![Meshtastic Grafana](./pictures/evaluation_grafana.png)

Description

1. Sun gone. The power path circuit disables direct powering from the solar cell. 
2. Discharge process over night
3. First sunlight. Battery charging starts.
4. Battery full. Power Path circuit disables the battery and switches to direct pass-through.

Using that graph the maximum survival time of the device without sunlight an be calculated.

- Start voltage, night: 4.1V

- Stop voltage, early morning: 4.04V

- Assumed hard switch-off voltage: 3.4V

- Duration: 12h

This leads to an average remaining battery run time of theoretically 128h (5.3 days). Pratically this would be more around 3-4 full days.
