#!/usr/bin/env python3

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GLib


class Notification():
    @staticmethod
    def sendNotification(name, icon, value):
        Notify.init("i3_tools")
        notif = Notify.Notification.new(name, icon=icon)
        if 'x-canonical-private-synchronous' in Notify.get_server_caps():
            notif.set_hint_string("x-canonical-private-synchronous", "true")
            notif.set_hint('value', GLib.Variant.new_int32(value))
        else:
            notif.update(name, "Value is set to %d" % value, icon=icon)
        notif.show()
