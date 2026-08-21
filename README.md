# MessagesDelivery

This project aims to build a message delivery system from the ground.
In the end, it will be made of several versions of itself, each one 
being an improvement of the last one. The first version will be as 
naive as possible and the goal is to reach an architecture close to
what can be implemented for WhatsApp even though only basic technologies
will be used and the least number of external librairies possible.

## Proportion of LLM in this project

As time goes by, it seems more and more important to be transparent
about the usage of generative AI in projects. This project has been
using ChatGPT 5.6 Luna on a Free-Tier account to discuss impletation
choices. The front part of the first version of this project was coded 
manually. However, Claude Sonnet 5 on a Free-Tier account has been used
to build the front version for the nexts versions.
All the code has been written by hand and some parts have been reviewed 
or corrected if the errors couldn't be resolved otherwise.

## Usage

This project uses Docker to build containers that interacts with each 
others. In order to start this project, you will need to execute the
command : 
```bash
docker compose up --build
```
This will automatically start all the containers if Docker (either
Engine or Desktop) is installed on your computer.

## First version (V1) - Naive

### TL;DR

This first version is the most naive possible. It contains a login/signin 
page and a page where you can create, select and delete a chat as well as
sending messages to a chat. You can also add people to the chat. Multiple
accounts can be signed up on the same browser profile.
However, you can't log out, you can't remove members of a chat, you can't
remove a message from a chat, you can't customize neither chat nor a 
profile and you need to click on a chat to see the new messages. As its
name suggests, its a naive approach.

### Content

It is made of 5 services whom two are already built services : Postgres 
and Nginx. Postgres is used to store messages and users and Nginx is 
used a reverse proxy.
Then comes the front service, it displays the web pages. The auth 
service is the service that rules the user tables of the database,
issues tokens for the users and verify the tokens while navigating the 
endpoints. Finally, the message service rules the message and chat tables
of the database. It is a basic Chat, Message and Chat Members database 
schema.
