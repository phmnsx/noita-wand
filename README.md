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
Builds and comments are created based on the User id and the .txt file, and of course based on what the user wishes to create. The code takes these inputs to make a dictionary in the correct database and assigns it values for identification, mainly ID and author-id.
Builds and comments are deleted based on their ownership and ID, the code detects if the person looking at the post is it's owner and if they are, it shows them the delete button, which, searches the post by ID on its database then deletes it (or, in the case of comments, pretends its deleted).
Spells from the game were also downloaded (via code, or some by hand) from their wiki at https://noita.wiki.gg/wiki/Noita_Wiki. And the spell's IDs are used for their identification.
Users have the property of "liked posts" and "builds", that tell the code what posts and builds the user has liked and created.
The code also adds layers to comments, for example, if i comment directly in a build, it's layer will be 0, but if i comment under a comment, it's layer will be 1 and so on. It's used to keep the page organized for when (complex!) discussions occur.
Also, if a build has been given no name, the code will automatically give it a name.

### The Frontend
A principal ideia desse projeto é ser uma ferramenta software de busca e criação de builds para o jogo Noita, para isto, consideramos dois tipos de usuários - visitantes e usuários logados onde visitantes possuem acesso apenas as ferramentas de pesquisas e o usuários logado, as ferramentas de busca e criação de builds. Para exercer as funções desse projeto em software foram idealizadas quatro telas: tela de pesquisa e resultados com e sem filtro de título, tela de pesquisa e resultados com filtro de spells, tela de criação de builds, tela do usuário com as builds criadas e curtidas pelo usuário.

Para o desenvolvimento dessa ferramenta o meio web foi decidico como o mais adequado, então já definimos o uso da linguagem de marcação HTML, com o Backend construido em Python escolhemos, por fim, o Flask, principalmente pela sua capacidade de atuar como um intermediário entre o Frontend e Backend e pela suas dependencias como o Jinja que facilitam a construção de páginas dinâmicas. Ainda nas tecnologias usadas, para autenticação de usuários logados ao invés de nossa ferramenta ter um sistema de cadastro de usuário se decidiu usar a API do Github para obtermos uma validação ao login do usuário e dados não-sensivéis do mesmo.

Com as ideias e tecnologias decididas foram colocadas as seguintes articulações no Frontend: HTML/CSS para a demarcação da páginas e seus estilos, Javascript para formatação da página e realizar chamadas aos Flask e, por fim, o Flask realizando o trafégo de dados do Backend para Frontend de forma formatada para o HTML/CSS, vale denotar que todas as páginas em que há resultados de builds foram construídas para que esses resultados apareçam para o usuário de forma dinâmica e em tempo real usando principalmente o Javascript articulado com o Flask.

Ainda no processo de desenvolvimento uma grande peça foram os resultados das builds que além de serem uma ilustração das builds deveriam conter funcionalidade de curtidas e acesso ao autores da build, para os usuários logados funcionalidade de comentários e respostas à essas build, para os autores das builds a funcionalidade de deletar a build e para os autores de comentários e respostas a funcionalidade de deletar seu comentário. Como resultados obtemos o seguinte layout completo para as builds:

![Alt text](/static/example_1.jpg?raw=true "Ilustration of a build's layout")
