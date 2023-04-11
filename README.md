
![Logo](https://user-images.githubusercontent.com/110100322/221649400-126d697b-5f4d-46e4-a58b-ef75a5e70e93.png)

## Table of content

- [Humanoid robot *BETA*](#humanoid-robot-beta)
- [Built with](#built-with)
- [Used libraries](#used-libraries)
- [Contruction](#contruction)
- [Servo control](#servo-control)
  - [Disclaimer](#disclaimer)
  - [Pulse Servo](#pulse-servo)
  - [Bus Servo](#bus-servo)
  - [Future plans](#future-plans)
- [Application](#application)
- [Speech-to-text](#speech-to-text)
- [Pose estimation](#pose-estimation)

---

## Humanoid robot *BETA*

BETA is an ambitious undertaking that seeks to develop a humanoid robot possessing a range of human-like capabilities, including the ability to walk, see, and communicate verbally.

Conceived in 2018, the project has undergone several transformations and upgrades over the years. Presently, it is being developed as part of the "[Koło Naukowe Humanoid](https://www.facebook.com/KNHStyleOfficial)" student scientific association, where updates on its progress and new features are regularly shared.

<p align="center">
  <img src="https://user-images.githubusercontent.com/110100322/230668078-4c8fa947-df42-4cb7-8807-3819f159b147.gif" width=60%>
</p>

---

## Built with

- [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- [Raspberry Pi display](https://www.dfrobot.com/product-1784.html)
- [Bus servos](https://en.ocservo.com/?post_type=products&page_id=16170)
- Pulse servos: [RDS3235-180](https://pl.aliexpress.com/item/32734965011.html?spm=a2g0o.order_list.order_list_main.173.29321c247JQ9SQ&gatewayAdapt=glo2pol) and [RDS3115-270](https://pl.aliexpress.com/item/32270225462.html?spm=a2g0o.order_list.order_list_main.172.29321c24tig7ZX&gatewayAdapt=glo2pol)
- USB Webcam
-

## Used libraries

- [PySide2](https://pypi.org/project/PySide2/) - GUI toolkit used in [Application](#application)
- [Selenium](https://www.selenium.dev/) - automation of browser used in [Speech-to-text](#speech-to-text)
- [OpenCV](https://opencv.org/) - real-time computer vision used in [Pose estimation](#pose-estimation)
- [OCServo](https://github.com/Shinnken/OCServo_App/) - servo control app used in [Servo control](#servo-control)
- [pigpio](https://pypi.org/project/pigpio/) - control of GPIO to generate software PWM signal to control [Pulse servos](#disclaimer) servos.

---

## Contruction

The framework of the robot is composed of a hybrid of components that are either 3D-printed, purchased, or self-fabricated. The design of these parts was created in Blender, a 3D modeling software, and subsequently constructed by our team.

<p align="center">
  <img src="https://i.imgur.com/RL8Mg1e.png" width=60%>
</p>

Additionally, a 3D printer was utilized to produce the robot's chest component.

---

## Power supply

Humanoid robot BETA is powered by a combination of two step-up voltage regulators that convert 5V to 6V and 5V to 12V respectively. While this power supply configuration is functional, it is not an ideal solution for providing power to the robot's components. As such, we plan to upgrade the power supply to a more efficient and stable configuration that uses step-down voltage regulators to convert 12V to 5V and 12V to 6V respectively.

The proposed power supply solution involves the use of a 3-cell lithium-ion battery. The nominal voltage of a typical 3-cell lithium-ion battery is 11.1 volts (3.7 volts per cell). However, the actual voltage of a fully charged lithium-ion battery can range from 12.6 volts (4.2 volts per cell) to 9.0 volts (3.0 volts per cell) when fully discharged.

By using a step-down voltage regulator to convert the 12V output from the battery to 5V and 6V respectively, we can ensure a stable and efficient power supply for the robot's components. This power supply solution also provides the added benefit of making the robot battery-powered, which increases its mobility and versatility.

We are confident that this proposed power supply solution will provide a safe, efficient, and reliable source of power for Humanoid robot BETA, and we look forward to implementing this upgrade in the near future.

---

## Programming language

The programming language of choice for the project is Python. This decision was made because of its ease of use, large community, many libraries and frameworks and cross-platform compatilibity. Additionally, Python is a versatile language that can be used to develop a wide range of applications, including those that are used for the control of the robot's servos, the implementation of its vision system, and the development of its speech recognition and speech-to-text capabilities.

---

## Servo control

As previously stated, our project utilizes two distinct types of servos. Due to their differing control mechanisms, we have partitioned their descriptions into two distinct subcategories.

### Disclaimer

Our use of the term "pulse" refers to a conventional servo that employs a Pulse Width Modulation (PWM) signal as its control input.

### Pulse Servo

Using mentioned library we've created tool to control servos with single commands.
To affix the servos to the robot's framework, we employ brackets that are included in the kit alongside the servos. The Raspberry Pi's GPIO pins serve as the source of the PWM signal, which is generated by utilizing the software [pigpio library](https://pypi.org/project/pigpio/). We have developed a tool utilizing the aforementioned library, which allows for the control of the servos through the use of single commands.

<p align="center">
  <img src="https://i.imgur.com/VPsad9d.png" width=50%>
</p>

During the process of developing the robot, it became apparent that the existing servos were not ideally suited to our requirements, as they were prone to excessive play and struggled to maintain a fixed position. As a result, we made the decision to incorporate [Bus servos](#bus-servo) in the leg joints, as these offer superior stability and control. By leveraging this approach, we can enhance the overall performance and reliability of the system, while enabling greater precision and accuracy in its movements.

### Bus Servo

In regards to the management of the second group of servos, communication is established through the utilization of the UART protocol, as the servos in question incorporate internal electronics. This approach enables efficient transmission of commands and data, as well as simplifying the wiring and control of the servos. By interfacing with the internal electronics of the servos, the system can achieve greater precision and flexibility in its movements.

<p align="center">
  <img src="https://i.imgur.com/7DqY3fH.png" width=50%>
</p>

For more information about Bus servo control check out our [Servo library](https://github.com/Shinnken/OCServo_App/)

### Sequencial movement

To achieve smooth movement we've created tool that allows to control servos in sequence. It's main purpose is to control servos in sequence to achieve smooth movement.

*INTERT DETAILED DESCRIPTION OF SEQUENTIAL MOVEMENT*

### Future plans

As part of our future development plans, we intend to upgrade the current servos with more powerful alternatives. This enhancement will enable the creation of more intricate and sophisticated movements. In addition, we plan to incorporate a more advanced control system, which will allow for the implementation of more complex behaviors and actions.

---

## Application

The software application that has been developed utilizes the PySide2 library to create a graphical user interface (GUI). The primary objective of this application is to enable the user to manage and manipulate the behavior of a robot through a touch screen interface.

<p align="center">
  <img src="https://i.imgur.com/bkVHds5.png" width=48%>
  <img src="https://i.imgur.com/EkO7Dwt.png" width=50.5%>
</p>

---

## Speech-to-text

For the purpose of speech-to-text, we have utilized the speech to textV website. The website is accessed through the use of the Selenium library. The library allows for the automation of the browser, which enables the implementation of the speech-to-text functionality.

One possible solution to address this issue is to utilize an application programming interface (API) that provides speech-to-text functionality. However, after careful consideration, it was determined that this approach was not optimal due to cost implications and implementation complexity. As an alternative, a solution was chosen that is both cost-effective and easy to implement, and does not impose excessive demands on computer resources.

---

## Pose estimation

For the purpose of pose estimation, the project team has chosen to use ArUco trackers, which are part of the OpenCV library. This is because ArUco markers are an efficient and accurate type of fiducial marker that can be easily detected and identified in image or video streams. By attaching multiple ArUco markers to the robot's limbs and joints, the position and orientation of these markers can be tracked to estimate the robot's pose with a high degree of accuracy.

<p align="center">
  <img src="https://i.imgur.com/AFKgGQ0.jpg" width=50%>
</p>

In order to collect information about the location and orientation of the human body's joints and calculate angles for the robot, ArUco trackers will be attached to the human body. At this time, no other solutions have been selected for pose estimation purposes. However, the project team is considering adding gyroscope sensors to provide a more accurate source of information for angle estimation, thus allowing the robot to replicate human movements more accurately. Furthermore, a combination of different solutions, such as ArUco trackers, 2D pose estimation, and gyroscopes, may be tested to determine which approach yields the best results.

---

## Safety precautions

While operating humanoid robot BETA, it is important to take the necessary safety precautions to prevent injury or damage to the robot or its surroundings. Please read the following guidelines carefully before using the robot:

    Supervision: Always supervise the robot when it is in use. Do not leave the robot unattended around small children or pets.

    Operating environment: Use the robot in a safe and controlled environment. Avoid using the robot near stairs, ledges, or other hazards that could cause the robot to fall or be damaged.

    Power source: Only use the power source specified in the documentation. Do not use unauthorized power sources or chargers, as this could damage the robot or cause a fire.

    Servo control: When controlling the robot's servos, be aware of their range of motion and potential speed. Do not exceed the recommended range or speed, as this could damage the robot or cause it to malfunction.

    Maintenance: Regularly inspect the robot for wear and tear such as loose screws, frayed wires, or damaged components. If any issues are found, take the necessary steps to repair or replace the affected parts.

    Transport: When transporting the robot, make sure it is securely fastened and protected from damage.

By following these safety precautions, you can help ensure the safe and reliable operation of your humanoid robot BETA.