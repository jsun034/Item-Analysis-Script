# Item Analysis Python Script


## Purpose

This script is useful in determining which multiple choice questions are good predictors of free response scores. If we can create an exam with questions that are good predictors of FRQ scores, teachers would have no need for free response exams. Thus, the grading process would be simplified without any compromises.


## Running the Script

* A ".csv" file containing exam details must be passed in the command-line. This includes each student's multiple choice response,  answer choices, MC score, FR score, and the answer key.  Refer to "example_data_file.csv" for the formatting. 
* A ".csv" file named "results.csv" will be generated. This file will contain data such as mean FRQ scores of students who answered correctly, correlation of each question with FRQ scores, and KR-20. 
* ex// python examAnalysis.py example_data_file.csv


## File Descriptions

* examAnalysis.py: code for item analysis
* example_data_file.csv: example of how student exam data should be entered


## License

This project is licensed under the GNU General Public License v3.0.  See "LICENSE" for details.
