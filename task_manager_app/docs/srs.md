# Software Requirments Specification
## For Task Manager
Version 1.1
Prepared by Andy Ewell
Group 4
02/11/1026
## 1. Introduction

### 1.1 Document Purpose
This is the document for explaining system requirments
not for how it will be implemented. The Primary users
will be average people needing to organize their goals.

### 1.2 Scope
The Task Manager will be used for managing personal tasks
and so a user can organize tasks and stay on track for personal
goals. It will allow for logging and setting reminders for tasks
along with setting up a schedule for accomplishing them. Potential
for buisness level task managing in the future.

## 1.3 Definitions
__SRS__: Software Requierments Specification document for explaining app requirments

__UI__: User Interface for user to interact with app.

__GUI__: Graphical User Interface for accessable and visual user interface

## 1.4 Refrences
vision_plan by Drew Howard  
version 1.0  
INFORMATIVE  
https://github.com/RovagugsKnight/G4_To_do_list/blob/main/task_manager_app/docs/vision_plan.md

Use Case by Drew Howard  
version 1.1  
02/11/2026  
INFORMATIVE  
https://github.com/RovagugsKnight/G4_To_do_list/blob/main/task_manager_app/docs/G4%20Group%20Project%20-%20Use%20Case.svg

## 1.5 Document Overview
- Product Overview: Provides background and context for product requirements.
- Requirements: Requirements for product.
- Verification: Describes on requirments will be verified.
  
# 2. Product Overview
## 2.1 Product Perspective
This is a new application not part of any larger system. Ownership of this product and all 
related documentation resides with Group 4. 

## 2.2 Product Functions
- Logging tasks
- Removing tasks
- Editing tasks
- Viewing tasks
- Setting task deadlines
- Giving task reminders  
Use Case Diagram:   
https://github.com/RovagugsKnight/G4_To_do_list/blob/main/task_manager_app/docs/G4%20Group%20Project%20-%20Use%20Case.svg

## 2.3 Product constraints
No constraints, no limits, no rules just managing tasks

## 2.4 User Characteristics
__User Class: Registered User__
- __Role__: Uses all product features 
- __Expertise__: Low to moderate computer literacy
- __Access Level__: All product features including cloud services?
- __Frequency of Use__: Few times a week or every day
- __Accessibility Needs__: Intutive navigation and responsive layout
- __Goals__: Organizing, storing, and setting deadlines for many tasks

__User Class: Guest User__
- __Role__: Uses part of product features
- __expertise__: Low to moderate computer literacy
- __Access Level__: Some product features like logging tasks locally
- __Frequency of Use__: Every once in a while
- __Accessibility Needs__: Same as registered user
- __Goals__: Same as registered user with less tasks

## 2.5 Assumptions and Dependencies
__Assumption__: The system will use the Kivy framework for GUI development.  
__Dependency__: Continued support of the Kivy library.  
__Potential Impact__: A change in the GUI framework would require a major redesign
of front end design.

## 2.6 Apportioning of Requirments
Release 1: Product documentation
Release 2: Product Diagrams and class design
Next Release requirements unknown

# 3. Requirements
## 3.1 External Interfaces
__Hardware Interfaces: This system does not require interaction
from specialized hardware devices.__

### 3.1.1 User Interface
__REQ-FUNC-001-0.1__  
__Add Task Button__  
The system shall have an add task
button to allow users to create a new task
and add it to the tasklog.  
Acceptance Criteria:  
- Button will be visible to user
- When button is pressed add task function executed

Verification: Test

__REQ-FUNC-002-0.1__  
__Delete Task Button__  
The system shall have a delete task
button to allow users to delete tasks
from the tasklog.  
Acceptance Criteria:
- Button will be visible to user
- When button is pressed delete task function executed

Verification: Test

__REQ-FUNC-003-0.1__  
__Task Completion Checkbox__  
The system shall have a Checkbox
to mark a task completed.  
Acceptance Criteria:
- Checkbox will be visible to user
- A checkbox will be included for every task

Verification: Test

### 3.1.2 Software Interface

__REQ-COMP-001-0.1__  
__Kivy Framework__  
The system shall use the
Kivy framework to create the 
applications GUI.    
Acceptance Criteria:
- The system runs Kivy without errors
- The GUI is implemented using Kivy widgets and layouts

Verification: Inspection

## 3.2 Functional Requirements








