# RENCI Ventilator
## The RENCI Ventilator project

This project represents the specification and prototype of a ventilator design by Dr. Kirk Wilhelmsen MD, PhD.

The system utilizes a Raspberry Pi 4 to:
-	Control aspects of the system, 
-	Poll, collect and store data from various sensors 
-	Provide a user interface to monitor its' function.

The user interface is implemented with a Django website that utilize ventilator data to provide feedback to the patient.

### Installation:

Perquisites:
* Python3.8
* Django >= 3
* django-cors-headers

