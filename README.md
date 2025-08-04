# ranime
Find random anime from https://randomanime.org

> [!NOTE] 
> A terminal emulator with support for either Kitty graphics or iTerm2
> graphics protocol is recommended.

![](https://files.catbox.moe/2st1aa.png)

# Installation
```shell
pip install git+https://github.com/eeriemyxi/ranime
```

# Usage
```
ranime --auth-token <AUTH_TOKEN> --id <id>
```

It automatically saves the auth token and id for the subsequent runs, so you can
just do `ranime` from then on.

# Guide
## Getting Auth Token
Open DevTools (inspect element) on your browser, go to Network tab, then in that
state, go to https://randomanime.org and create a new list. Then grab the
authentical token as shown below:

![](https://files.catbox.moe/jat1xu.png)

## Getting ID
Generate a new list on https://randomanime.org with your preferences then pick the ID from the URL:

![](https://files.catbox.moe/s7wpg5.png)
