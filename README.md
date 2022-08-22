# TinyML-Footprint

## TinyML Footprint Calculator — *Coming Soon*
Plug in play calculator for measuring footprint of complete TinyML system in progress and will be available soon (i.e. before camera-ready deadline)!

## Raw Data 
Below is the embodied fooprint in kg CO2-eq for each component of a TinyML System for 3 different applications using Pirson & Bol [[1]](#1). Model Training numbers taken from Dodge et al. [[2]](#2) using DenseNet models, which serve as an upper bound as these models are much larger, and require more energy to train, than typical TinyML models. To account for the Use-Stage of the hardware life cycle (i.e. operational footprint) included below, we calculated the kg CO2-eq of recharging the power supply  using emission factor for electricity consumed from EPA [[3]](#3), accounting for three years (to be consistent with Apple’s analysis [[4]](#4)) of continuous use at 1 mW, an average estimate of the power used by current TinyML systems in the MLPerf Tiny Benchmark [[5]](#5), [[6]](#6). End-of-life stage taken to be negliblige contribution (i.e. <1%) to system footprint as shown in multiple similar cases such as Apple Watch [[4]](#4) and STMicroelectronics Microcontroller [[7]](#7).
![Alt text](./TinyMLSystems_Footprint_Data.png?raw=true "Title")

## Hardware Specification Level Selection for TinyML Systems 
Pirson & Bol [[1]](#1) breakdown any IoT device into generic functional blocks: processing, memory, actuators, casing, connectiv-
ity, PCB, power supply, security, sensing, transport, user interface, and others circuit components (e.g. resistors, capacitors, diodes, etc.). Within
these blocks, there are different specifications that need to be met depending on the application and its requirements. To show our footprints are reasonable, here we explain our selections for each TinyML System component from the specification levels provided in the image below from Pirson & Bol [[1]](#1). All three TinyML application footprints shown above (i.e. Keyword Spotting, Anomaly Detection, and Image Classification) contain the same system components *except* for the sensing modules as  sensing requirement is different for each application. Note that in our paper we have only included Keyword Spotting (best case) and Image Classification (typical case & worst case) to capture the range of TinyML System footprints while limiting text appropriately. 
![Alt text](./HSLs_Pirson_Bol_2021.png?raw=true "Title")

#### Actuators (HSL-0)
No actuators are typically needed in the context of TinyML systems, especially not in the applications outlined earlier. Typically TinyML is used to perform on-device sensor analytics that can then relay some information to another system to take appropariate action. 

#### Casing (HSL-1)
Ideally TinyML should be able to be deployed in a "stick-and-peel" fashion, making the form factor and casing required very small. However, a 50-100g platic encasing as specified in HSL-1 is more than enough, and even in 10g in most cases ideally. For reference [here](https://www.aliexpress.com/item/2251832572097825.html?gatewayAdapt=4itemAdapt) is what 100g ABS plastic case look like as outlined in HSL-1 upper bound for this component. 

#### Connectivity (HSL-0)
One of the main premises of TinyML is running the ML on device, rather than being reliant on the cloud. That being said some minimal communication will always be needed. However, typically we do not see an external IC for communication on TinyML systems and the communication embedded in the processor as mentioned in HSL-0 is what is used and is sufficient. 

#### Memory (HSL-0)
TinyML is performed on MCUs with only KBs of memory. This fits HSL-0 for this category; a separate, external chip for memory is not typical in TinyML. See Zhang et al. [[8]](#8) for examples of MCUs with only KBs of memory running TinyML. HSL-0 should suffice for most TinyML applications. 

#### Others (HSL-0)
Other circuit components (e.g. resistors, capacitors, diodes, etc.) are not needed for running TinyML and HSL-0 is sufficient for this category. 

#### PCB (HSL-0)
The Arduino Nano 33 BLE Sense is built specifically with the intent of running TinyML [[9]](#9). The printed circuit board (PCB) can be found to be 8.1 square centimeters, showing HSL-0 for this component is sufficient. 

#### Power Supply (HSL-2)
A typical lithium ion battery for the power assumed to run TinyML (i.e. 1mW) on device will allow the systems to run for years with recharge required at a practical interval, compared to say a coin cell battery. The calculations performed to conclude this assumed a battery with 3.6V nominal voltage running at 2000 milliamp hours which we found to be reasonable and typical for a lithium-ion battery. 

#### Processing (HSL-0)
HSL-0 includes a standalone MCU. All other HSLs include an application processor which is not necessary and needed for running TinyML. 

#### Security (HSL-0)
Separate ICs for security (i.e. HSL-1) are not typically found in TinyML devices. We find any security embedded in the processing (i.e. HSL-0) is sufficient at the moment and more common.

#### Sensing (HSL-1, HSL-2, HSL-3)
The sensing hardware specification level differed depending on application. For keyword spotting a microphone (i.e. HSL-1) is sufficient. Typically anomaly detection involves some sort of fusion of sensors (i.e. HSL-2). Finally, image classification requires a camera (i.e. HSL-3). 

#### Transport (HSL-1)
The total weight of the TinyML system, even assuming 100g for casing in the worst case, should fall between the range provided per TinyML device in HSL-1 for transporting

#### User Interface (HSL-1)
An UI is not typically needed for TinyML systems since humans are not typically interacting much with these systems once deployed in the wild but some LEDs or switch buttons should be sufficient to interact or signal anything to the user. For this reason, we selected HSL-1 for this component. 


## References
<a id="1">[1]</a> 
Pirson, T., & Bol, D. (2021). Assessing the embodied carbon footprint of IoT edge devices with a bottom-up life-cycle approach. Journal of Cleaner Production, 322, 128966.

<a id="2">[2]</a> 
Dodge, J., Prewitt, T., Tachet des Combes, R., Odmark, E., Schwartz, R., Strubell, E., ... & Buchanan, W. (2022, June). Measuring the Carbon Intensity of AI in Cloud Instances. In 2022 ACM Conference on Fairness, Accountability, and Transparency (pp. 1877-1894).

<a id="3">[3]</a> 
https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references

<a id="4">[4]</a> 
https://www.apple.com/in/environment/pdf/products/watch/Apple_Watch_Series7_PER_Sept2021.pdf

<a id="5">[5]</a> 
C. Banbury, et al., “Mlperf tiny benchmark,” in Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks, J. Vanschoren and S. Yeung, Eds., 2021.

<a id="6">[6]</a> 
https://mlcommons.org/en/inference-tiny-07/

<a id="7">[7]</a> 
https://www.st.com/content/st_com/en/about/st_approach_to_sustainability/sustainability-priorities/sustainable-technology/eco-design/footprint-of-a-microcontroller.html

<a id="8">[8]</a> 
Zhang, Y., Suda, N., Lai, L., & Chandra, V. (2017). Hello edge: Keyword spotting on microcontrollers. arXiv preprint arXiv:1711.07128.

<a id="9">[9]</a> 
https://store-usa.arduino.cc/products/arduino-nano-33-ble-sense
