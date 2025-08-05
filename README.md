# ranime
Find random anime from https://randomanime.org

This small project addresses an issue with the site that had been bothering me
for a while. The site doesn't let you save the current progress when you view a
generated list, so the next time you'd want to pick a random anime, you'd either
have to create another list (which is time-consuming because you have to
reselect the preferences) or go back to that position yourself.

There is also the Spinner feature but it's unnecessarily slow and suffers
from the same problems.

> [!TIP] 
> A terminal emulator with support for either Kitty graphics or iTerm2
> graphics protocol is recommended.

![](https://files.catbox.moe/2st1aa.png)

# Installation
```shell
pip install git+https://github.com/eeriemyxi/ranime
```

# Usage
```
ranime --auth-token <AUTH_TOKEN> --id <ID>
```
> [!NOTE]
> It automatically saves the authentication token and ID for the subsequent runs, so you can
> just do `ranime` next time.

# Guide
## Getting Authentication Token
Open DevTools (inspect element) on your browser, go to Network tab, then in that
state, go to https://randomanime.org and create a new list. Then grab the
authentication token as shown below:

![](https://files.catbox.moe/jat1xu.png)

## Getting ID
Generate a new list on https://randomanime.org with your preferences then pick the ID from the URL:

![](https://files.catbox.moe/s7wpg5.png)
