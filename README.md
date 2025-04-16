# ExcelReaderBot
User can upload excel file to telegram bot, bot save the excel file, read it and return content from this excel file to user. 
Program parsing price of items from urls and xpath.

## How to run
1. Clone the repository
2. Create virtual environment `python -m venv venv`
3. Activate virtual environment `source venv/bin/activate` or `venv\Scripts\activate`
4. Create .env file and add your token from botfather, and name of db file like in .example.env
5. Install the dependencies `pip install -r req.txt`
6. Run the bot `python main.py`

## How to use
1. Run the bot
2. Click on the button "Загрузить файл"
3. Send the excel file to the bot
4. Bot will return the content of the excel file
