# hotenov.com

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)][badge-license]

## About

This project is dedicated to my personal website.
I've decided to have a "mono" repository
where the backend part *(Django)* is located in the `src` subfolder
and the frontend *(without any JS framework yet)* - in the `src_front` subfolder.

I shared the code in December 2023 and at that time
it contained the copy of my "static" version of the site (from 2019)
plus the Resume app that I have written to learn basics of Django Framework.

So, having it in public I can easily demonstrate my skills (or lack of them 😃)
and my progress on learning web development.

## 🛠️ Requirements

- Python 3.12+  
- Poetry 1.7+  
- Node.js 14+  
- Docker or PostgreSQL 16 server

## 💻 Installation

If you want to run this website locally,
first you need to get the source code.

```plain
git clone https://github.com/hotenov/hotenov.com.git
cd hotenov.com
```

Second, build common static files.

### Build static files

```plain
npm install
npm run build
```

### Run local debug server

(without Docker)

1) Specify your PostgreSQL database credentials in `_DockerStuff/.env.dev.local`
(all `SQL_*` environment variables)

2) Install dependencies  

    ```plain
    poetry install
    ```

3) Activate your virtual environment

    ```plain
    poetry shell
    ```

4) Run Django debug server

    ```plain
    python src/manage.py runserver 8887
    ```

If you have Docker installed on your machine,
you can spin up two containers: debug server and PostgreSQL server.  
*(However, you still need to build static files outside Docker.
I plan to add a separate service for that someday)*

### Run DEV container

*(optional)* You can edit `_DockerStuff/.env.boilerplate`
and change debug server port via `WEB_PORT` variable (default is `8833`)

Execute the following command:  
*(If you are on Linux host, add `sudo` at the beginning)*

```plain
docker compose -f _DockerStuff/docker-compose.yml up
```

## 📝 License

Distributed under the terms of the [MIT license](https://opensource.org/license/mit/), the source code of **hotenov.com** is free and open source software. It means you can modify it, redistribute it or use it however you like as long as you do mention the author of the original script.

## 🙏🏻 Credits

The Resume app was inspired by [wagtail-resume](https://github.com/adinhodovic/wagtail-resume)
plug-in (by [Adin Hodovic](https://github.com/adinhodovic)).

I borrowed CSS layout for resume from [Coding Market](https://www.youtube.com/@CodingMarket)'s
YouTube [video](https://www.youtube.com/watch?v=c9Yn20h2Jxw)
and a few styles from another [video tutorial](https://www.youtube.com/watch?v=hnjHCmaUVPg)
by [Online Tutorials](https://www.youtube.com/@OnlineTutorialsYT) channel.

I integrated a couple of web components from [codyhouse.co](https://codyhouse.co/)
owned by Amber Creative S.R.L.

[GitHub Profile Card](https://github.com/piotrl/github-profile-card) by [Piotr Lewandowski](https://github.com/piotrl)

The initial "static" website was based on [Clean Blog](https://github.com/StartBootstrap/startbootstrap-clean-blog) blog theme,
created by [Start Bootstrap](https://startbootstrap.com/).

Many JS and CSS snippets from the Internet *(see attribution in comments to the code)*.

<!-- Reference Links -->
[badge-license]: https://github.com/hotenov/hotenov.com/blob/main/LICENSE.md
