# Noita Builds
### Video Demo: 
https://www.youtube.com/watch?v=_c1IK22G8Eg
### Description:
A site for sharing your favorite Noita builds.
## The idea
To get the idea for the project, i thought about something i like to do something based off of it. Thinking about this for some time, i've realized no onehad ever made a website dedicated to sharing builds for the game "Noita", where you can help both new and old players by sharing whatever crazy/fun buildsyou can come up with, each build having a title and a description, and obviously, the spells needed.

### The planning
First, i got someone who had better understanding of html than i do, so i teamed up with user "Marco-Aurelio-256", who would work in the frontend and i in the backend. We discussed where we would store the database for the website, and also some design choices, for example, the homepage and search modes. We settled for using .json as databases and also using both "search by name" and "search by spell" as the two search modes. But we also thought people might like checking out some person's likes or builds they've done, so, we also implemented profiles that will display all of the user's builds and liked builds.
We also discussed if comments should truly be deleted or only show up as deleted for moderation's sake. We thought people might send something bad then delete it and then we wouldn't know what bad has been typed, so we don't actually delete comments in case we need them for something.

### The backend
For this project i needed to learn to manipulate dictionaries and lists (with dictionaries in them), how to use .json files
spells.py was made specifically to let the website access the spells database
create.py was made specifically to handle builds and its actions (Creating, reading, updating, deleting) (CRUD)
main.py was made for every other aspect, such as comments, reports, and searching
I also needed to account in errors that might happen so the program wouldn't return something undesirable. I also had to create a .txt file that would act as some sort of global variable, which would be saved even if the code stopped running and could be accessed by multiple files, in order to maintain a consistent ID assignement to posts and comments.

Builds and comments are created based on the User id and the .txt file, and of course based on what the user wishes to create. The code takes these inputs to make a dictionary in the correct database and assigns it values for identification, mainly ID and author-id.
Builds and comments are deleted based on their ownership and ID, the code detects if the person looking at the post is it's owner and if they are, it shows them the delete button, which, searches the post by ID on its database then deletes it (or, in the case of comments, pretends its deleted).
Spells from the game were also downloaded (via code, or some by hand) from their wiki at https://noita.wiki.gg/wiki/Noita_Wiki. And the spell's IDs are used for their identification.

Users have the property of "liked posts" and "builds", that tell the code what posts and builds the user has liked and created.
The code also adds layers to comments, for example, if i comment directly in a build, it's layer will be 0, but if i comment under a comment, it's layer will be 1 and so on. It's used to keep the page organized for when (complex!) discussions occur.
Also, if a build has been given no name, the code will automatically give it a name.

### The Frontend
For the purposes of the site, we considered two types of users - visitors and logged-in users, where visitors have access only to the search tools and logged-in users to the search and build creation tools. To carry out the functions of this software project, four screens were designed: search screen and results with and without title filter, search screen and results with spells filter, build creation screen, user screen with builds created and liked by the user.

For the development of this tool, the web environment was decided to be the most suitable, so we already defined the use of the HTML markup language, with the Backend built in Python we finally chose Flask, mainly for its ability to act as an intermediary between the Frontend and Backend and for its dependencies such as Jinja that facilitate the construction of dynamic pages. Still on the technologies used, instead of our tool having a user registration system, we decided to use the Github API to validate the user's login and non-sensitive data. 

With the ideas and technologies decided, the following links were put in place on the Frontend: HTML/CSS for demarcating the pages and their styles, Javascript for formatting the page and making calls to Flask and, finally, Flask performing the data traffic from the Backend to the Frontend in a formatted for HTML/CSS, it is worth noting that all the pages where there are build results were built so that these results appear to the user dynamically and in real time using mainly Javascript linked with Flask.

Another major part of the development process was the build results, which, as well as being an illustration of the builds, should contain the functionality of likes and access to the build authors, for logged-in users the functionality of comments and replies to these builds, for the build authors the functionality of deleting the build and for the authors of comments and replies the functionality of deleting their comment. As a result, we get the following complete layout for the builds:


![Alt text](/static/example_1.jpg?raw=true "Ilustration of a build's layout")
