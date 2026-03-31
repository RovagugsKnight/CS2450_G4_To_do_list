## Scenario 1 (Creating a task): 
    Steps to recreate: 
        1. Open app, 2. Type in task name, description, and deadline, 3. Select category button, Click the plus button.
    Expected output:
        I expect that a new card will appear underneath the add task bar with the name, description, and deadline I just entered.
        Task card will be category color.
    Actual output:
        Output was as expected.
    Screenshot:
![Creating a task](validation_scenarios_screenshots/filling%out%form.png)

![Task Displayed](validation_scenarios_screenshots/new%task.png)

## Scenario 2 (Saving a task with no name):
    Steps to recreate: 
        1. Open app, 2. Dont type in task name, 3. Click the plus button.
    Expected output:
        I expect an error to show up telling me that I need to enter a name.
    Actual output:
        Output was as expected.
    Screenshot:
![No name](validation_scenarios_screenshots/no%name.png)

## Scenario 3 (Saving a task with no description):
    Steps to recreate: 
        1. Open app, 2. Type in task name with no description, 3. Click the plus button.
    Expected output:
        I expect that a new card will appear underneath the add task bar with the name no description.
    Actual output:
        Output was as expected.
    Screenshot:
![No description](validation_scenarios_screenshots/no%description.png)

![No card description](validation_scenarios_screenshots/no%description%fine.png)

## Scenario 4 (Deleting a saved task):
    Steps to recreate: 
        1. Create task 2. click the minus button on the task to delete.
    Expected output:
        I expect that the task will dissapear and the othe tasks (if any) will slide over to fill the gap left by the deleted task. 
    Actual output:
        Output was as expected.
    Screenshot:
![Before Delete](validation_scenarios_screenshots/before%delete.png)

![After Delete](validation_scenarios_screenshots/after%delete.png)

## Scenario 5 (Completing a saved task):
    Steps to recreate: 
        1. Create task, 2. Click done on the task you just created.
    Expected output:
        I expect the task to stay there, but the done button to darken to let me know the task has been completed.
    Actual output:
        It worked as expected.
    Screenshot:
![Completing a task](validation_scenarios_screenshots/task%done.png)

## Scenario 6 (Edit task):
    Steps to recreate: 
        1. Create task, 2. Click edit on task you just created, 3. Change text inputs and category, 4. Press save button.
    Expected output:
        I expect the tasks text values to change based on my input. I expect card color to change to the color I selected.
    Actual output:
        It worked as expected.
    Screenshot:
![Before Edit](validation_scenarios_screenshots/before%edit.png)

![Before Save](validation_scenarios_screenshots/before%save.png)

![After Edit](validation_scenarios_screenshots/after%edit.png)

## Scenario 7 (Create Category):
    Steps to recreate: 
        1. Click hamburger menu, 2. Select 'Create Category', 3. Input name and select color, 4. click submit.
    Expected output:
        I expect the category to show up as an option for creating tasks.
    Actual output:
        It worked as expected.
    Screenshot:
![Before creation](validation_scenarios_screenshots/before%category.png)

![Creating](validation_scenarios_screenshots/creating%category.png)

![After creation](validation_scenarios_screenshots/after%category.png)

## Scenario 8 (Delete Category):
    Steps to recreate: 
        1. Click hamburger menu, 2. Select 'Delete Category', 3. select category, 4. click submit.
    Expected output:
        I expect the category to dissapear as an option for creating tasks.
    Actual output:
        It worked as expected.
    Screenshot:
![Before deleting](validation_scenarios_screenshots/before%deleting%category.png)

![Deleting](validation_scenarios_screenshots/deleting%category.png)

![After deleting](validation_scenarios_screenshots/after%deleting%category.png)


