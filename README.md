# CRLS clubfinder

## Run the site
To run the site, clone this repository and copy the following commands in the directory terminal:

```
% pip install -r requirements.txt
```
```
% python3 main.py
```

## About the project

#### Find, join, leave, and create clubs for the CRLS community.

I created this website for CRLS students to have an easier place to find clubs. Currently we only find out about clubs on club day at the start of the year. This website makes it so year round, students can join new clubs as soon as their schedule changes. It allows students to view descriptions and see what the club is about directly from the website, without having to rely on secondhand information. 

Leaders can post pictures and accomplishments from their club to convince new members to join. 

I will work with the school to make the process of creating your own clubs much faster and more streamlined. The current process is very timeconsuming. 

If you have any ideas or questions regarding the website and its functionality, let me know by emailing me at **25ranjaria@cpsd.us.**

## About the code

This project uses Flask, a lightweight Python framework. 

- The database uses SQL, but Flask allows SQL queries to be written in Python, using the library SQLAlchemy. 
- All the button functionality is controlled by JavaScript.
- Styling is done by CSS.
- HTML handles the layouts.
  - Flask uses its own templating language, Jinja, which allows files to be "extended" or copied by other files for simplicity and time management.
- The themes at the top of the page are actually done 98% by CSS, as each color is a variable and clicking on one theme changes the value of every color variable. This is part of the reason why there is so much CSS in the project. 
  - JavaScript is used to store the color theme the user selects in the ```localStorage```, so when the page reloads or the user exits the theme stays in place. 
- Flask allows variables to be passed from the backend (Python) into the frontend (HTML). 
  - Every time a club is created, it gets added the database class **Club**. This is stored by SQL. Instead of a list of each club getting passed to the frontend, the backends send the entire **Club** *class* to the frontend. 
    - Ex: 
  
        ```Python
        return render_template("layout.html", club_info=Club.query.all(), user=current_user)
        ```
        This return statement redirects the user to the file "layout.html" (home page) and sends in all the information that is in the **Club** class in the variable *club_info*. The *user* variable sends the current user's information to "layout.html." Now, in the "layout.html" file, I can access all of the passed in information with the templating language Jinja. 

        - Ex: 
            ```Python
            {% for club in club_info %}
                        <div class="club" id="{{ club.club_name }}1">
                            <div class="clubcontent" id="{{ club.club_name }}"> 
                                <div class="clubtitle" id="{{ club.club_name }}1">{{ club.club_name }}</div> 
            {% endfor %}
            ```
            This is just an example; the actual code is longer, but the idea is that I can loop through the *club_info* and select content from the **Club** class to fill in the card information. (Note: the id names help to identify information for the JavaScript functions). 
            
            Because the number of clubs are technically unknown, I can't hardcode each card into the "layout.html" file. I only have one card template, and I use Jinja to loop through the **Club** class via the variable *club_info*. Each time a new club is added, it gets added to the **Club** class, and because the class is being looped through every time "layout.html" is loaded, the new club gets automatically added to the home page. 

  - Every time a user joins a club, that club gets added to the **joined_clubs** table in the **models.py** file. This table links the two other database classes, **User** and **Club**, which each store all the information about the subject. **joined_clubs** stores foreign keys, or links to both clubs, in that table. So when a user joins *Drone Club* for example, the id for the **User** who joined and the id for *Drone Club* gets stored in **joined_clubs**. A completed model looks something like this:

    ```Python 
    Political Awareness Club
    [<User 2>, <User 1>, <User 3>]
    ---
    Debate Club
    [<User 3>]
    ---
    Media Arts Club
    [<User 2>, <User 1>]
    ---------------------
    25ranjaria@cpsd.us
    [<Club 1>, <Club 2>]
    ---
    rehaan1099@gmail.com
    [<Club 3>, <Club 6>, <Club 4>, <Club 2>]
    ---
    kshfkjds@gmail.com
    [<Club 1>, <Club 2>]
    ---
    ```
    Every **Club** can have as many *unique* members (the same member can't join the same club more than once), and every **User** can join as many *unique* clubs. This relationship is modeled in a many-to-many relationship between the database models **User** and **Club**.

    Leaving clubs is very simple. The id for the user who left and the id for the club they're leaving both get deleted from the **joined_clubs** table. 
    - Ex: 
        ```Python
        current_user.clubs.remove(Club.query.filter_by(club_name=leave_club).first())
        ```
        The name *clubs* is how the table **joined_clubs** gets referenced by the **User** class. The **Club** class references **joined_clubs** as *members*.