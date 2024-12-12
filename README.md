# Task Management Bot for Telegram

[<img src="https://img.shields.io/badge/Telegram-%40Scoop-blue">](https://t.me/Scoop_it_Bot) ![Version](https://img.shields.io/badge/version-1.0.0-blue)  ![License](https://img.shields.io/badge/license-MIT-green)


This repository contains the source code of a minimalistic telegram bot for managing the user's personal tasks. The goal of the project was to create an understandable and uncomplicated service inside Telegram (which for many users is the #1 application in terms of time spent daily), which would not be functionally inferior to well-known analogues from large corporations.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Used Technology](#used-technology)
4. [Installation](#installation)
5. [License](#license)
6. [Contribution](#contribution)
7. [Future Plans](#future-plans)

## Features
* Task Management:
  - 'Create the task' button allows task creation with various parameters.
  - 'My tasks' button shows the user's current tasks.
  - 'Today tasks' button displays today's tasks.
  - Notifications at set times with multiple options to handle them.
* Commands:
  - '/start' command to launch or restart the bot.
  - '/tips' command to access a quick guide.
  - '/feedback' command to send bug reports or feedback to the admin.
  - '/admin' button provides statistics and a list of usernames.
* Timezone setting via the 'Send location' button.

## Used technology
* Python [3.12](https://www.python.org/downloads/release/python-3120/)
* aiogram [3.10](https://pypi.org/project/aiogram/3.10/) (Telegram Bot framework)
* aiogram-dialog [2.1](https://aiogram-dialog.readthedocs.io/en/stable/) (GUI framework for Telegram Bot);
* Docker and Docker Compose [latest](https://www.docker.com/products/docker-desktop/); (containerization);
* Redis [7.4](https://redis.io/download); (cashe and persistent storage for user states);
* NATS JetStream [latest](https://nats.io) (as a broker);
* PostgreSQL [15-alpine](https://www.postgresql.org/download/) (DB);
* SQLAlchemyORM [2.0.32](https://docs.sqlalchemy.org/en/20/orm/) (ORM lib for DB interactions);
* Alembic [1.13.2](https://pypi.org/project/alembic/1.13.2/) (DB migrations);

## Installation
### Requirements
- Installed Git, Docker, and Docker Compose.
1. **Create a directory**
Create a directory for the bot. For example: '/Users/Name/my_bot'. 
2. **Clone a repository**
Open the terminal inside the created directory and run the command:
```bash
git clone https://github.com/agrikol/task-management-telegram-bot.git
```
3. **Set your secrets**
Rename the '.env.example' file to '.env'. Then, following the instructions inside it, put your secrets there.
4. **Run your bot**
Open the terminal inside the bot directory and run the command:
```bash
docker compose up --build
```
5. **Check the logs**
If something goes wrong, log messages inside the terminal will answer your questions.
6. **Get started**
Open Telegram, find the bot, and initiate the `/start` command to begin managing your tasks.

## Licence
This project is distributed under the MIT license. You are free to use, modify, and distribute the code, as well as contribute to its development (which I would greatly appreciate).

## Contribution
Your contribution is more than welcome! Feel free to open an issue with suggestions, feature requests, or bug reports.
Here's how you can get started:

1. **Fork the repository**  
Click the "Fork" button to create a copy of this repository in your account.
Clone it to your local environment and create a new branch for your changes:  
```bash
git clone <repository_url>
cd <repository_folder>
git checkout -b feature/your_feature_name
```
2. **Make some changes**
Implement your changes, whether it’s fixing a bug, adding a new feature, or some improvements.
3.	**Submit a pull request**
Once your changes are ready, push them to your forked repository:
```bash
git commit -am "Description of the change"
git push origin feature/your_feature_name
```
Then open a pull request to the main branch of this repository.

Your contributions are absolutely appreciated, whether it's a small bug fix or a major feature!


## Future Plans
The following features are planned to be added in the future
* Tasks sorting
* Display of completed tasks
* Localization (English, French, German, Spanish)
* Recurrent Task (Task schedule) 
* Better logging
* Improving admin panel
* Speech-to-Text probably (for task data voice entering)
The project needs your ideas and suggestions!
Thanks for reading!
