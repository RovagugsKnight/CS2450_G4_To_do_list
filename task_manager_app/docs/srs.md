# Software Requirments Specification
## For Task Manager
Version 1.1  
Prepared by Andy Ewell  
Group 4  
02/11/1026
## Table of Contents
<!-- TOC -->
* [1. Introduction](#1-introduction)
    * [1.1 Document Purpose](#11-document-purpose)
    * [1.2 Product Scope](#12-product-scope)
    * [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions)
    * [1.4 References](#14-references)
    * [1.5 Document Overview](#15-document-overview)
* [2. Product Overview](#2-product-overview)
    * [2.1 Product Perspective](#21-product-perspective)
    * [2.2 Product Functions](#22-product-functions)
    * [2.3 Product Constraints](#23-product-constraints)
    * [2.4 User Characteristics](#24-user-characteristics)
    * [2.5 Assumptions and Dependencies](#25-assumptions-and-dependencies)
    * [2.6 Apportioning of Requirements](#26-apportioning-of-requirements)
* [3. Requirements](#3-requirements)
    * [3.1 External Interfaces](#31-external-interfaces)
    * [3.2 Functional](#32-functional-requirements)
    * [3.3 Quality of Service](#33-quality-of-service-non-functional-requirements)
    * [3.4 Compliance](#34-compliance-non-functional-requirements)
    * [3.5 Design and Implementation](#35-design-and-implementation-non-functional-requirements)
* [4. Verification](#4-verification)
<!-- TOC -->

## 1. Introduction

### 1.1 Document Purpose
This is the document for explaining system requirments
not for how it will be implemented. The Primary users
will be average people needing to organize their goals.

### 1.2 Product Scope
The Task Manager will be used for managing personal tasks
and so a user can organize tasks and stay on track for personal
goals. It will allow for logging and setting reminders for tasks
along with setting up a schedule for accomplishing them. Potential
for buisness level task managing in the future.

## 1.3 Definitions
__SRS__: Software Requierments Specification document for explaining app requirments

__UI__: User Interface for user to interact with app.

__GUI__: Graphical User Interface for accessable and visual user interface

## 1.4 References
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

## 2.6 Apportioning of Requirements
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
application's GUI.

Acceptance Criteria:
- The system runs Kivy without errors
- The GUI is implemented using Kivy widgets and layouts

Verification: Inspection

## 3.2 Functional Requirements

#### REQ-FUNC-004-0.1  
__Task Log__

The system shall store
tasks in a persistent
task log.

Acceptance Criteria:
- Tasks remain stored in task log after system is closed and restarted
- Tasks can be retrieved and viewed from task log by the user.

Verifcation: Test

__REQ-FUNC-005-0.1__    
__Add Tasks__

The system shall allow users
to add tasks to the task log, 
including a name, description,
and an optional deadline.

Acceptance Criteria:
- Tasks appear in tasklog
- Tasks contain specified details

Verifcation: Test

__REQ-FUNC-006-0.1__  
__Delete Tasks__

The system shall allow users
to delete selected tasks from the task log.

Acceptance Criteria:
- Specified tasks are gone from task log

Verfication: Test

__REQ-FUNC-007-0.1__  
__Edit Tasks__

The system shall allow users
to modify the name, description, or
deadline of a selected task and save
the updated task to task log.

Acceptance Criteria:
- Updated name, description, or deadline appear in saved task
- modifications match users changes

Verification: Test

__REQ-FUNC-008-0.1__  
__Categorize Tasks__

The system shall allow users
to organize tasks into a named
group.

Acceptance Criteria:
- Task displays category name
- Task is included in category group

Verification: Test

## 3.3 Quality of Service (Non-Functional Requirements)

### 3.3.1 Performance

__REQ-PERF-001-0.1__  
__Local Task Log Retreival__

The system shall retrieve a task
log of up to 10,000 tasks from local storage 
within 10 ms under normal operating conditions.

Applies to: [REQ-FUNC-004-0.1](#req-func-004-01)

Acceptance Criteria:
- Task log is loaded into local memory within 10 ms

Verfication: Test

### 3.3.2 Security
__No security requirements currently. Authentication and encryption for future system.__

### 3.3.3 Reliability

#### REQ-REL-001-0.1
__Invalid Input Handling__

The system shall reject invalid user input 
without terminating the application process.

Acceptance Criteria:
- Application remains running after invalid input is submitted
- No uncaught exceptions are raised
- Existing task data remains intact

Verification: Test

#### REQ-REL-002-0.1
__Data Preservation on Failure__

The system shall retain all automatically saved task 
changes after an unexpected shutdown.

Acceptance Criteria:
- All tasks in local storage when system isn't running.

Verification: Test

### 3.3.4 Availability

#### REQ-AVAIL-001-0.1
__Access Offline__

The system shall allow users to
access task log while offline.

Acceptance Criteria:
- Task log is accessible while offline.

Verification: Inspection

### 3.3.5 Observability

## 3.4 Compliance (Non-Functional Requirements)

## 3.5 Design and Implementation (Non-Functional Requirements)

### 3.5.1 Installation

### 3.5.2 Build and Delivery

### 3.5.3 Distribution

### 3.5.4 Maintainability

### 3.5.5 Portability

### 3.5.6 Deadline

### 3.5.7 Proof of Concept

### 3.5.8 Change Management

# 4. Verification

| Requirement ID | Verification Method | Test/Artifact Link | Status | Evidence           |
|----------------|---------------------|--------------------|--------|--------------------|
|REQ-FUNC-001-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-FUNC-002-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-FUNC-003-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-FUNC-005-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-FUNC-006-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-FUNC-007-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-FUNC-008-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-COMP-001-0.1|      Inspection     |      document      |Planned |                    |
|REQ-PERF-001-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-PERF-001-0.1|         Test        | [tests](src\tests) |Planned |                    |
|REQ-REL-001-0.1 |         Test        | [tests](src\tests) |Planned |                    |
|REQ-REL-001-0.1 |         Test        | [tests](src\tests) |Planned |                    |
|REQ-AVAIL-001-0.1|     Inspection     |      document      |Planned |                    |
