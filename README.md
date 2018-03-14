Website users activity simulator
====================================

This app can help you to simpulate users activation of users.
It simulates users loading random pages
and spending random time on every page. 


Usage
-----

To start this app. Simply use

> python app.py "yourwebsiteaddres"

i.e.:

> python app.py https://softarm.pl


Details
-------

This app uses live loaded proxy server addresses to simulate users from many locations.

App assumes that many proxies are wrong, so will immedietely close threds with unusefull proxies.


Tested on the following websites: 

- [https://softarm.pl](https://softarm.pl)

