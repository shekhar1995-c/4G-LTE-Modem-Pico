# 4G LTE Modem Pico Project

Successfully wrapped up the hardware design for a custom 4G LTE modem board based on the Quectel EC200 module. Sharing the PCB layout view for fellow engineers, designers, and makers interested in connected hardware design.

## Design Overview

- **Core Feature:** Designed around Quectel EC200 for cellular connectivity (LTE CAT 1).
- **Power Delivery:** Clean path with 12V input, ferrite filtering, and proper bulk decoupling.
- **ESD Protection:** Full USB ESD protection (TPD2EUSB30) + ferrite bead & capacitor filtering to meet EMI/EMC best practices.
- **Signal Integrity:** Proper ground plane stitching and vias under critical components to improve signal return paths and reduce noise.
- **Mechanical Stability:** Mounting holes tied to GND for shielding and better mechanical grounding.
- **Connectivity:** Multiple antenna ports: Main, GNSS, and WiFi.
- **Flexibility:** Debug/test points, SIM interface, and key GPIOs for easy integration.
- **Manufacturability:** Thoughtful component placement and spacing for serviceability and production readiness.
- **Tools & Validation:** Developed and validated entirely in EasyEDA with 3D and DRC analysis.

## Additional Highlights

This design was a deep dive into EMC, signal integrity, and practical hardware engineering, culminating in a board ready for real-world deployment. The 4-layer stackup and meticulous routing reflect months of iteration, ensuring reliability under demanding conditions.

I also integrated a Raspberry Pi Pico with I2C to collect sensor and temperature data, sending it to the server in real-time.

---

Feel free to explore, give feedback, or collaborate!

---

## License

*(Add your preferred license here, e.g. MIT License)*

---

#PCBDesign #4GModem #Quectel #IoT #HardwareEngineering #EasyEDA #SignalIntegrity #EMCDesign #ElectronicsDesign
