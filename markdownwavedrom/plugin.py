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


# Copied from https://github.com/facelessuser/pymdown-extensions/blob/a8fb9666566dfb7e86094082860b5616885d35f4/pymdownx/superfences.py#L83
def _escape(txt):
    """Basic html escaping."""

    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    txt = txt.replace(">", "&gt;")
    return txt


# for pymdownx
def fence_wavedrom_format(source, language, class_name, options, md, **kwargs):
    return '<script type="WaveDrom">%s</script>' % (_escape(source))


class WavedromConfig(mkdocs.config.base.Config):
    embed_svg = mkdocs.config.config_options.Type(bool, default=False)
    pymdownx = mkdocs.config.config_options.Type(bool, default=False)


class WavedromPlugin(BasePlugin[WavedromConfig]):
    def on_pre_build(self, config, **kwargs):
        if "embed_svg" in self.config:
            self.embed_svg = self.config["embed_svg"]
        else:
            self.embed_svg = False
        if "pymdownx" in self.config:
            self.pymdownx = self.config["pymdownx"]
        else:
            self.pymdownx = False

    def on_post_page(self, output_content, config, **kwargs):
        if self.pymdownx:
            # bs4 is slow in parsing large html, use string instead
            if "WaveDrom" in output_content:
                output_content = output_content.replace(
                    "</body>",
                    "<script>window.addEventListener('load', function() {WaveDrom.ProcessAll();});</script></body>",
                )
            return output_content

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

        # pymdownx
        if len(soup.find_all("script", type="WaveDrom")) > 0:
            f_exists = True

        if f_exists and not self.embed_svg:
            new_tag = soup.new_tag("script")
            new_tag.string = (
                "window.addEventListener('load', function() {"
                "WaveDrom.ProcessAll();});"
            )
            soup.find("body").append(new_tag)

        return Text(soup)
