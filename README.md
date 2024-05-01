# Noita Builds
### Video Demo:
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
