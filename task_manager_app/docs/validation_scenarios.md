# Scenario 1 (Creating a task): 
    Steps to recreate: 
        1. Open app, 2. Type in task name and description, 3. Click the plus button.
    Expected output:
        I expect that a new card will appear underneath the add task bar with the name and descriptions I just entered.
    Actual output:
        It had the output I expected.
    Screenshot:
        ![Creating a task](../docs/validation_scenarios_screenshots/Create%20task%20w%20name%20and%20desc.png)

# Scenario 2 (Saving a task with no name):
    Steps to recreate: 
        1. Open app, 2. Dont type in task name, 3. Click the plus button.
    Expected output:
        I expect an error to show up telling me that I need to enter a name.
    Actual output:
        It had the output I expected.
    Screenshot:
        ![No name](../docs/validation_scenarios_screenshots/Create%20task%20w%20no%20name.png)

# Scenario 3 (Saving a task with no description):
    Steps to recreate: 
        1. Open app, 2. Type in task name with no description, 3. Click the plus button.
    Expected output:
        I expect that a new card will appear underneath the add task bar with the name no description.
    Actual output:
        It had an error saying that we needed a task description. We need to edit this so it works with just a task name.
    Screenshot:
        ![No description](../docs/validation_scenarios_screenshots/Create%20task%20w%20no%20desc.png)

# Scenario 4 (Deleting a saved task):
    Steps to recreate: 
        1. Open app, 2. Type in task name and description, 3. Click the plus button, 4. click the minus button on the task to delete.
    Expected output:
        I expect that the task will dissapear and the othe tasks (if any) will slide over to fill the gap left by the deleted task. 
    Actual output:
        For the most part this worked just fine, but if I deleted enough tasks I sometimes got a gap in the cards instead of them sliding over to fill the gaps. We need to correct the spacers in the code.
    Screenshot:
        ![Deleting task](../docs/validation_scenarios_screenshots/Delete%20a%20saved%20task.png)

# Scenario 5 (Completing a saved task):
    Steps to recreate: 
        1. Open app, 2. Type in task name and description, 3. Click the plus button, 4. Click done on the task you just created.
    Expected output:
        I expect the task to stay there, but the done button to darken to let me know the task has been completed.
    Actual output:
        It worked as expected.
    Screenshot:
        ![Completing a task](../docs/validation_scenarios_screenshots/Complete%20a%20task.png)

