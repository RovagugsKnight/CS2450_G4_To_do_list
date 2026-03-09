# Refactoring Notes

## Milestone 3:
- Added task name option for task input
- created card layout for tasks with modification buttons on the sides
- cards are split evenly into rows of 3
- task name can be edited
- reorganised code so view is exclusively view logic and controllers handle business logic
- Made task repository into an abstract class for dependency inversion and to make
project more scalable
- Sqlrepo is the task repository type being used
- added docstrings, typehints, and comments
