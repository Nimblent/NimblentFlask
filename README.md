<div align=center>

# Nimblent

![](https://img.shields.io/badge/python-v3.11+-blue)

NSI web project with [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) and the Flask and SQLObject modules

Python https://www.python.org/

Flask documentation https://flask.palletsprojects.com/

SQLObject documentation https://www.sqlobject.org/

# Setup
</div>


## Downloading

You can download the project from [here](https://github.com/Nimblent/NimblentFlask/archive/refs/heads/master.zip) or by cloning the repository with the following command:


```bash
git clone https://github.com/Nimblent/NimblentFlask.git
```

## Start the project


1.  Open a command prompt in the project directory (downloaded and extracted before)
2.  Write `py main.py` in the terminal



All necessary modules will be automatically installed at first startup through the `requirements.txt` file

## Access the website and create a school
You can access the website through [127.0.0.1:8000](127.0.0.1:8000)  
You'll first need to create a school by providing a name, a french RNE number and a password.  

![Startup image](https://media.discordapp.net/attachments/1188187232918581419/1207072044278222888/image.png?ex=65de5071&is=65cbdb71&hm=f5e587fde8c89366166a3afe17664b34fff4af8db9a9711d00d7899b52daee9f&=&format=webp&quality=lossless&width=1025&height=458)

<div align=center>

# How to use

</div>

## Login

The login page is accessible directly from the home/index page `/`  
You can login with the school's RNE number as username and the password you provided when creating the school or with any other account you created.
![login page](https://media.discordapp.net/attachments/1188187232918581419/1207073673769517086/image.png?ex=65de51f6&is=65cbdcf6&hm=855564e6302956302e068321f12d5aa86cf7553dd66bb086553d19816a96b911&=&format=webp&quality=lossless&width=1025&height=459)

If the user you logged in with is a teacher, or an admin you'll access the admin dashboard.

## Add users - Admin dashboard
![Add user](https://media.discordapp.net/attachments/1188187232918581419/1207075330591039569/image.png?ex=65de5381&is=65cbde81&hm=779adc48b3fdbd3e966f14e54c11f8006cc10a293961b0720e5fe990e07904e5&=&format=webp&quality=lossless&width=1025&height=465)

Click on the "Add user" button to add a new user.

![Add user form](https://media.discordapp.net/attachments/1188187232918581419/1207075909006397510/image.png?ex=65de540b&is=65cbdf0b&hm=d9f3bbe6ca253062e6405bfda93a6fc589465d684f604b42d65858604da70eb8&=&format=webp&quality=lossless&width=1025&height=454)

On the form, you can choose the user's role, the user's name, the user's login name, and the user's password. User's login name and password will be used to [login to the website](#login).

## Add course - Admin dashboard

**As admin only** (RNE login) you can add a course to the school for specific students.

![Add course](https://media.discordapp.net/attachments/1188187232918581419/1207079335950024825/image.png?ex=65de573c&is=65cbe23c&hm=e3519774016c17bd9a0660a0755403af06589ee4b97447b3b31b1829f1fe426b&=&format=webp&quality=lossless&width=1025&height=458)

![Add course form](https://media.discordapp.net/attachments/1188187232918581419/1207080919257841724/image.png?ex=65de58b5&is=65cbe3b5&hm=d5e6b2c34b2a73f00d61d6708178a2b254dac382053f74d2894b24386954c981&=&format=webp&quality=lossless&width=1025&height=458)

You can choose **multiple teachers and multiple students** for the course by clicking on the user while holding the `ctrl` key.


## Retrieve courses - Admin dashboard
There is no direct way to retrieve courses from the admin dashboard, but you can download the **current user**'s courses in a `.ics` file by clicking on the "Télécharger l'emplois du temps" button (logged in as a teacher or a student with accounts created before).

You can then import the `.ics` file in your calendar application or use [this website to preview the schedule](https://larrybolt.github.io/online-ics-feed-viewer)



<div align=center>

# Credits

</div>

- [**noappertBD (Nolan APPERT)**](https://github.com/noappertBD)
- [**firelop (Pierre GUCHET)**](https://github.com/firelop)
- [**NoveltyDust0 (Nathanaël QUERAUD)**](https://github.com/NoveltyDust0)
