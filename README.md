# ilil

`ilil` is an insta-like image log. It uses the 
[bottlepy](https://github.com/bottlepy/bottle) framework and builds a website
featuring various basic functions for sharing pictures, just like Insta but free! :^)


## Features

- Built-in `bottlepy` web server.
- Uploading pictures and generating thumbnails.
- Adding description texts for the pictures.
- `config.toml` for configuring information such as title, contact information,
  port, backend password, items per page, enabling download.
- Pagination, based on `itemsPerPage` variable in `config.toml`.


## Installation


```bash
pip install bottle Pillow numpy toml # dependencies to install
git clone https://github.com/riotbib/ilil.git
cd ilil

cp config.toml.example config.toml
vim config.toml # edit variables, every variable needs to be provided
python ilil.py
```


## To Do

- `default.nix` for providing and configuring the service on
  [NixOS](https://nixos.org).
- Parsing thumbnail size variable from `config.toml`.
- Function for deleting images and descriptions.
- Function for editing descriptions (for now please edit `data.toml` with care).
- Filters! (No joke.)
