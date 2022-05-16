# GRE vocab schedule generator

A python script to generate vocabulary learning schedule using Ebbinghaus learning curve. Current vocab sets includes `GRE佛脚`, `GRE等价词汇`, `镇考3000`, and `镇考机经词汇`.



## Schema

We define a **card** as the combination of **term + definition**. Term and definition should be separated by `-`, and **cards** should be separated by `\n\n`. 

This schema should be applied to all vocab lists and Quizlet import.



## Add vocab sets 

User can add more vocab sets than default sets by simply create a new directory. Inside that directory, make sure every vocab list file is of type `.txt` and follows the schema defined above



## Quizlet import

Default output directory `每日任务` is under the same directory `schedule_generator.py`. User need manually import each vocab list into quizlet manually using following steps

1. Create study set using [this url](https://quizlet.com/create-set)

2. Click `从Word、Excel、Google Docs等文件导入。` or `+ Import from Word, Excel, Google Docs, etc.`

3. Copy and paste vocab from one (or more) list

4. Modify `Between term and definition` to `-`, and modify `Between cards` to `\n\n`

   ![readme_2](readme_2.jpg)

5. Click `Import`

6. Click the first card, set `Term language` as `ENGLISH`, and set `Definition language` as `CHINESE (SIMPLIFIED)`

    ![readme_1](readme_1.jpg)

7. Finally, click `Create`