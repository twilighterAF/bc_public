Hello there, this web application was created to improve sellers experience with crypto exchange service bestchange.net.

How it works?
1. api_gateway receives zip file via bestchange API.
2. controller parse file and return json.
3. views send json to user, while main javascript inside main html page calling it.
4. Javascript parse json and create tables, that show all sort of needed information.
5. On the main page user also have sidebar, that provide some settings like: change pairs, change marked exchanger or change limit of showed exchangers inside each pair, also can choose city in table header.
6. Settings send to backend and storing inside json/user_filters.json. User settings applies in rate_processor function inside controller.py.


Short tour of the application.
1. API._call_status in api_gateway implemented because we don't want multiple users calls multiple API zipfile downloads. So while we have at least 1 client, status sets to True, else API._TIMELIMIT expires and API._api_loop sets status to False then loop stops.
2. When you just open app in browser zip file needs to be downloaded(if api_loop stopped). Estimate time ~ 10-15 seconds.
3. Main parse function is the rate_processor inside controller.py. It iterates through user_filters.json pairs then iterates through current pair with user settings like: limit of exchangers and city.
4. On the user side main.js in main.html calling for api_get_rates() in views.py that returns get_json_report() from controller.py.
5. Interval for calling was set at 10 seconds, can be changed on the bottom of the main.js.
