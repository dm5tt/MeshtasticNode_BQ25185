![MeshtasticRouterNode](pictures/MeshtasticNode_BQ25185.jpg)

## What is this thing?

This is a Meshtastic solar node based on the [Heltec HT-CT62](https://resource.heltec.cn/download/HT-CT62/HT-CT62(Rev1.1).pdf) and the (new) solar charge controller [TI BQ25185](https://www.ti.com/lit/ds/symlink/bq25185.pdf).

Features of this PCB

 - Solar Input up to 18V (24V survival)
 - 3A maximum load
 - 1A maximum charge current
 - Pseudo-MPPT (VINDPM)
 - Power Path (= if the battery is fully charged and there's enough solar power the device is getting powered directly from solar)
 - Two ADC pins to get battery (GPIO1) and solar (GPIO0) voltage using voltage dividers
 - 3.7V LiPo either via 18650 block or JST-PH 2.0 connector
 - Low power LDO [HEERMICR HE9073A33MR](https://www.lcsc.com/datasheet/lcsc_datasheet_2201242130_HEERMICR-HE9073A33MR_C723793.pdf)

Combined with a solar panel this device can be placed in remote areas to cover a wide range.

# Where can I get all the stuff?

Heltec HT-CT62: Aliexpress

TI BQ25185: Mouser or Digikey

PCB: You can load the Kicad project file and then export the manufacturing files using the plugins. Just throw them into JLCPCB and order them.

Everything else can be ordered from LCSC.

Due to strict legislation, it is not planned to offer ready-made circuit boards or kits here. Sorry.

# Do I have to modify the Software and configuration?

No. Only some smaller changes regarding the pin mapping is required.

```
diff --git a/variants/heltec_esp32c3/variant.h b/variants/heltec_esp32c3/variant.h
index ca00c43f..4f13248f 100644
--- a/variants/heltec_esp32c3/variant.h
+++ b/variants/heltec_esp32c3/variant.h
@@ -1,16 +1,13 @@
-#define BUTTON_PIN 9
-
-// LED pin on HT-DEV-ESP_V2 and HT-DEV-ESP_V3
-// https://resource.heltec.cn/download/HT-CT62/HT-CT62_Reference_Design.pdf
-// https://resource.heltec.cn/download/HT-DEV-ESP/HT-DEV-ESP_V3_Sch.pdf
-#define LED_PIN 2      // LED
-#define LED_STATE_ON 1 // State when LED is lit
-
 #define HAS_SCREEN 0
 #define HAS_GPS 0
 #undef GPS_RX_PIN
 #undef GPS_TX_PIN
 
+#define BATTERY_PIN 1
+#define ADC_CHANNEL ADC1_GPIO1_CHANNEL
+#define ADC_MULTIPLIER 2
+#define BATTERY_SENSE_SAMPLES 5
+
 #define USE_SX1262
 #define LORA_SCK 10
 #define LORA_MISO 6

diff --git a/variants/heltec_esp32c3/pins_arduino.h b/variants/heltec_esp32c3/pins_arduino.h
index a717a370..b8ebc09c 100644
--- a/variants/heltec_esp32c3/pins_arduino.h
+++ b/variants/heltec_esp32c3/pins_arduino.h
@@ -6,8 +6,8 @@
 static const uint8_t TX = 21;
 static const uint8_t RX = 20;
 
-static const uint8_t SDA = 1;
-static const uint8_t SCL = 0;
+static const uint8_t SDA = 18;
+static const uint8_t SCL = 19;
 
 static const uint8_t SS = 8;
 static const uint8_t MOSI = 7;

diff --git a/variants/heltec_esp32c3/platformio.ini b/variants/heltec_esp32c3/platformio.ini
index 6fe5c3c6..8087aa08 100644
--- a/variants/heltec_esp32c3/platformio.ini
+++ b/variants/heltec_esp32c3/platformio.ini
@@ -8,4 +8,6 @@ build_flags =
 monitor_speed = 115200
 upload_protocol = esptool
 ;upload_port = /dev/ttyUSB0
-upload_speed = 921600
\ No newline at end of file
+upload_speed = 921600
+board_build.f_cpu = 80000000L
```

When configuring the device you should set the "Minimum Wake Interval" from 10 seconds to 1 second.

Switch  Bluetooth and Wifi off! They suck power like crazy.


# Evaluation

[Evaluation, PCB v0.2 (CR123A)](./EVALUATION-v02.md)

# FAQ

*The HT-CT62 uses a ESP32C3. Thats not Low Power!!!*

Meshtastic  supports the "Power Saving" mode on the ESP32 where the entire   device stays  in the light sleep mode until it gets a interrupt signal from the LoRa modem. In that phase CPU will consume around ~800uA while sleeping. Including LoRa RX that's a idle draw around 2-4mA.

Still far away from the Wisblock. But who cares? During the day you will have a positive power budget so the entire devices runs on solar energy and recharges its battery. 

*It's not really that cheap either!*

Yep. It's expensive if you build only 1 device. But the costs dramatically drop if think of building 5-10 of them as you can mass order everything (PCBs, Components from LCSC and so own).

*The TI BQ25185 uses a linear regulator. That will be inefficient for solar panels above 6V.*

Yep. That's true. One of the major flaws of this design. 

There are other variants (TI BQ25620/BQ25622) that are using a Buck converter.

Most likely (untested) this will cause troubles during the winter time where 18V solar panels would be a great benefit.

This is going to be in a new design (as MeshtasticNode_BQ25185 is now fully tested) in a few months.

# Warning

LED circuit for STAT1 and STAT2 not yet tested. The TI BQ25185 uses 1.8V there so we need a transistor as switch.

# License

GPL v3
