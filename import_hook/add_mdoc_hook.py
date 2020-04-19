# -*- coding: utf-8 -*-
from import_hook import import_hook


class DocHacker(import_hook.Hook):
    def hack(self, module):
        module.__doc__ = "一个从渺小中走来，以伟大而结束的传奇。 -- Noaghzil.星辰之子"
        return module

import_hook.register(DocHacker())
