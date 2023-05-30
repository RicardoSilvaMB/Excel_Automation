This script enables you to optimize your time when you finish your pricing in AWS Calculator. Unfortunately, in this Beta version you can´t 
automate all the process, but only most of them.
DO NOT CHANGE THE CSV FILE NAME. Leave it as "My Estimate.csv" 
With this in mind, let´s start. 

1. First open your Linux Terminal and run the command below. You need to install all the necessary packages to run the script.

pip install -r requirements.txt

2. Open the csv you downloaded from aws calculator, and delete all the lines that are not either the header or the pricing rows.

3. Move your csv to queue folder. Is located in the main folder "Excel_Automation". 

4. With your Linux terminal open, go inside the main folder.

5. Run this command: python excel_automation.py

6. In file explorer, open the output folder. Inside is one excel file with the name "My Estimate - Phase 1". 

7. And we´re done. You just need to add the pricing calculator link, and the ec2 pricing model. This feature will come in the next update. 