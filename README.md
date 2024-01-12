# DM_Project
Discrete Mathematics Group Project ( Monsoon Semester 2023 )

Presentation Link: https://www.canva.com/design/DAFzji3TqdM/tNcCbVhqX3qb-ID9jUdKOg/edit?utm_content=DAFzji3TqdM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


## Install the required packages
```
pip install -r requirements.txt
```

## Run the Application
```
Run the Command: python interface.py

A Menu will appear in which you can choose the dimensions of the chess board as well as the algorithm that will be used to figure out the path.

A green trail indicates the knight managed to find a successful path, while a red one indicates that no path exists and the knight goes on the longest possible path.

Code and Python Constraints:
- Backtracking: This generally takes an exponential amount of time as the dimensions start increasing beyond 8x8.
- Warnsdorff: This starts taking a huge amount of time beyond 29x29.
- Divide and Conquer: Due to unpredictable behaviour of Qt library in Windows, it may start crashing at around 58x58, while its performance can be increased by using WSL. The algorithm works as far as 79x79, after which the code starts encountering the recursion limit in Python.
