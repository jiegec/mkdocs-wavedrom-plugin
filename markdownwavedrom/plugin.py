# Copyright (c) 2019, Shimoda <kuri65536 at hotmail dot com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from typing import Text
import mkdocs
from mkdocs.plugins import BasePlugin
from bs4 import BeautifulSoup
import wavedrom


class WavedromConfig(mkdocs.config.base.Config):
    embed_svg = mkdocs.config.config_options.Type(bool, default=False)


class WavedromPlugin(BasePlugin[WavedromConfig]):
    def on_pre_build(self, config, **kwargs):
        self.embed_svg = config["embed_svg"]

    def on_post_page(self, output_content, config, **kwargs):
        soup = BeautifulSoup(output_content, "html.parser")
        sections = soup.find_all("code", class_="language-wavedrom")

        f_exists = False
        for section in sections:
            f_exists = True
            if self.embed_svg:
                # render wavedrom to svg
                json = section.get_text()
                svg = wavedrom.render(json).tostring()
                new_soup = BeautifulSoup(svg, "html.parser")

                # embed svg into html
                section.parent.replace_with(new_soup)
            else:
                # replace code with script
                section.name = "script"
                section["type"] = "WaveDrom"
                # replace <pre>
                section.parent.replace_with(section)

        if f_exists and not self.embed_svg:
            new_tag = soup.new_tag("script")
            new_tag.string = (
                "window.addEventListener('load', function() {"
                "WaveDrom.ProcessAll();});"
            )
            soup.find("body").append(new_tag)

        return Text(soup)
