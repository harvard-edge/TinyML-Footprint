# TinyML-Footprint

## TinyML Footprint Calculator — *Coming Soon*
Plug in play calculator for measuring footprint of complete TinyML system in progress and will be available soon (i.e. before camera-ready deadline)!

## Raw Data 
Below is the embodied fooprint in kg CO2-eq for each component of a TinyML System for 3 different applications using Pirson & Bol [[1]](#1). Model Training numbers taken from Dodge et al. [[2]](#2) using DenseNet models, which serve as an upper bound as these models are much larger, and require more energy to train, than typical TinyML models. To account for the Use-Stage of the hardware life cycle (i.e. operational footprint) included below, we calculated the kg CO2-eq of recharging the power supply  using emission factor for electricity consumed from EPA [[3]](#3), accounting for three years (to be consistent with Apple’s analysis [[4]](#4)) of continuous use at 1 mW, an average estimate of the power used by current TinyML systems in the MLPerf Tiny Benchmark [[5]](#5), [[6]](#6). End-of-life stage taken to be negliblige contribution (i.e. <1%) to system footprint as shown in multiple similar cases such as Apple Watch [[4]](#4) and STMicroelectronics Microcontroller [[7]](#7).
![Alt text](./TinyMLSystems_Footprint_Data.png?raw=true "Title")

## Hardware Specification Level Selection for TinyML Systems 
Pirson & Bol [[1]](#1) breakdown any IoT device into generic functional blocks: processing, memory, actuators, casing, connectiv-
ity, PCB, power supply, security, sensing, transport, user interface, and others circuit components (e.g. resistors, capacitors, diodes, etc.). Within
these blocks, there are different specifications that need to be met depending on the application and its requirements. Here we explain our selections for each TinyML System component from the specification levels provided in the image below from Pirson & Bol [[1]](#1). All three TinyML application footprints shown above (i.e. Keyword Spotting, Anomaly Detection, and Image Classification) contain the same system components *except* for the sensing modules as  sensing requirement is different for each application. Note that in our paper we have only included Keyword Spotting (best case) and Image Classification (typical case & worst case) to capture the range of TinyML System footprints while limiting text appropriately. 
![Alt text](./HSLs_Pirson_Bol_2021.png?raw=true "Title")

#### Actuators (HSL-0)
No actuators are typically needed in the context of TinyML systems, especially not in the applications outlined earlier. Typically TinyML is used to perform on-device sensor analytics that can then relay some information to another system to take appropariate action. 

#### Casing (HSL-1)
Ideally TinyML should be able to be deployed in a "stick-and-peel" fashion, making the form factor and casing required very small. However, a 50-100g platic encasing as specified in HSL-1 is more than enough. For reference to see what 50-100g plastic cases look like see [here](https://www.alibaba.com/product-detail/15g-30g-50g-100g-Empty-Cosmetic_1600375933435.html?spm=a2700.7724857.0.0.1af332dfqd0A02).

#### Connectivity (HSL-0)


#### Memory (HSL-0)


#### Others (HSL-0)
Other circuit components (e.g. resistors, capacitors, diodes, etc.)

#### PCB (HSL-0)
Printed circuit board (PCB)

#### Power Supply (HSL-1)


#### Processing (HSL-0)


#### Security (HSL-0)


#### Sensing (HSL-1, HSL-2, HSL-3)


#### Transport (HSL-1)


#### User Interface (HSL-1)


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
Banbury, C., Reddi, V. J., Torelli, P., Holleman, J., Jeffries, N., Kiraly, C., ... & Xuesong, X. (2021). Mlperf tiny benchmark. arXiv preprint arXiv:2106.07597.

<a id="6">[6]</a> 
https://mlcommons.org/en/inference-tiny-07/

<a id="7">[7]</a> 
https://www.st.com/content/st_com/en/about/st_approach_to_sustainability/sustainability-priorities/sustainable-technology/eco-design/footprint-of-a-microcontroller.html
