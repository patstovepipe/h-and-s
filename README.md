#Data collection and management software 
## Built for a heart disease research charity.

####We are building software modules in Python 2.7 to complete the following tasks:
1. Grab human-written route descriptions from a spreadsheet. 
2. Interpret the route descriptions accurately, and make the user aware of unintelligible descriptions
3. Use the data from the descriptions to query an online database
4. Collect and organize the returned data into spreadsheets.

####This will allow the charity to have greater success in the absence of volunteers
The charity sends volunteer canvassers to knock on doors and ask for donations. Each canvasser has one or more "routes" to complete. A route 
consists of adjacent houses.

Think of how the average suburb in Victoria is laid out - Usually, it's a chaotic mess of streets intersecting plots of land at strange angles and very little 
consistency. If we want to create an easy, intuitive route for a canvasser, the best way is to inspect the streets by hand using a map and try seperate 
a given city block into small, walkable chunks. Since streets run for kilometers, but each block is more likely to be a square of 500m by 500m, we need 
to use multiple parallel and perpendicular streets to define a route. Thus, we need to decide what streets and addresses on each street define a route - 
what house do we start at and end at on each street, and are we going to stick to the left or right side (odd or even addresses)?

And so, the route description was born. Route descriptions look like this:

*110-160 Beach Dr Even#, 515-595 Falkland Rd Odd#, 2107-2135 McLaren Ave Odd#, 420-586 Victoria Ave Even#, 2116-2125 Hall Rd (40)*

Sometimes, they look like this:

*2851-2893 FOUL BAY Rd ODD#/2024-2090 ALLENBY St EVEN#/ 2029-2091 NEIL St ODD# (22)*

They can also look like this:

*Fairlane Terrace, Ascot Drive odds & evens 3704-3769,Queensbury 1300 & 1320 (35)*

As you can tell probably tell, **these route descriptions were compiled over a span of years and were written by different people who used different conventions.** 
This does not lend itself to easy parsing, but with some creativity, we can accurately extract the data from most of the route descriptions, and have humans deal with 
the ugly cases. Keep in mind that creating new route descriptions requires an unfeasable amount of time for a charity, organizations that, by definition, must have low
 overhead.

Now, we could just send the canvasser the route description and let them go! In most cases, they'll interpret it perfectly, and complete the route with no problems. 
But the route descriptions have another purpose: Recruiting canvassers. If a canvasser was from Saanich, it would be nice if they could canvass in Saanich;
 volunteers are *telerecruited* by calling the houses defined in the route descriptions of the routes they reside in. That means that we also have to collect 
phone numbers and names of the people in each route. For this purpose, a subscription to an online database is purchased.  

Every year the charity struggles to find volunteers to work through the 1,300 or so route descriptions by hand and compile spreadsheets containing this data.  
The success of their fundraising, and contribution to heart disease research, hangs on finding computer savvy people to complete the tedious, repetitive task of querying the online database with street names, copying down the addresses they want, and placing those in a spreadsheet.
This software will free them from this dependence on volunteers.

Though, it might make their office a lonelier place.
