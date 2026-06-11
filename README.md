# Python-Interactive-Dashboard

Source Data : Excel sheets
Requirements to Display in Dashboard :

1. Option to select data files : scenario “I will select two files, one right and one left”
2. Display data from both files respectively
3. Compare Serial_number column values
    a. matching values shown in green 
    b. Non-matching values shown in red 
4. Display : Total percentage of matching between both files <br>
If you are looking at the overall similarity between both sheets combined into one master pool (ignoring duplicates), look at the intersection over the union. <br>
Total unique rows across both sheets: (10 + 8 - 8 = 10 unique rows <br>
Formula: $\frac{8}{10} \times 100$ <br>
Result: 80%    

## Install dependencies

```
pip install -r requirements.txt
```

## Toosl used: 

Data : Excel data 
Dashboard : Python Dash Plotly library
