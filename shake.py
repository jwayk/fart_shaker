import obspython as obs
import time
from typing import Tuple

from animations import Wobble, Bulge, PlanarShake
from obs_tools import get_source_from_current_scene, HotkeyManager
from settings import (
    DEFAULT_SOURCE,
    DEFAULT_AMPLITUDE,
    DEFAULT_FREQUENCY,
    DEFAULT_DURATION,
    DEFAULT_DAMPING_FACTOR,
)


class Shaker:
    start_time = None
    trigger = False
    start_scale = obs.vec2()
    start_pos = obs.vec2()

    def __init__(
        self,
        source_name: str,
        wobble_animation: Wobble,
        scale_animation: Bulge,
        rattle_animation: PlanarShake,
    ):
        self.set_source(source_name)
        self.set_wobble(wobble_animation)
        self.set_bulge(scale_animation)
        self.set_rattle(rattle_animation)

    def shake(self):
        source = get_source_from_current_scene(self.source_name)
        if not source:
            return

        if self.trigger:
            if not self.start_time:
                obs.obs_sceneitem_get_scale(source, self.start_scale)
                obs.obs_sceneitem_get_pos(source, self.start_pos)
            self.start_time = time.time()
            self.randomize_shake()
            self.trigger = False

        frame = int(
            ((time.time() - self.start_time) / self.wobble.duration_seconds)
            * self.wobble.time.shape[0]
        )
        if frame >= len(self.wobble.transform_function):
            self.start_time = None
            return

        angle = self.wobble.transform_function[frame]
        obs.obs_sceneitem_set_rot(source, angle)

        new_scale = obs.vec2()
        scale_factor = self.bulge.transform_function[frame]
        new_scale.x = self.start_scale.x + scale_factor
        new_scale.y = self.start_scale.y + scale_factor
        obs.obs_sceneitem_set_scale(source, new_scale)

        new_pos = obs.vec2()
        x_displace = self.rattle.x.transform_function[frame]
        y_displace = self.rattle.y.transform_function[frame]
        new_pos.x = self.start_pos.x + x_displace
        new_pos.y = self.start_pos.y - y_displace
        obs.obs_sceneitem_set_pos(source, new_pos)

    def randomize_shake(self):
        self.rattle.randomize()

    def set_source(self, source_name: str):
        self.source_name = source_name

    def set_wobble(self, animation: Wobble):
        self.wobble = animation

    def set_bulge(self, animation: Bulge):
        self.bulge = animation

    def set_rattle(self, animation: PlanarShake):
        self.rattle = animation


hotkey = HotkeyManager()
shaker = Shaker(
    source_name=DEFAULT_SOURCE,
    wobble_animation=Wobble(
        amplitude=DEFAULT_AMPLITUDE,
        frequency=DEFAULT_FREQUENCY,
        duration_seconds=DEFAULT_DURATION,
        damping_factor=DEFAULT_DAMPING_FACTOR,
    ),
    scale_animation=Bulge(5, 10, DEFAULT_DURATION),
    rattle_animation=PlanarShake(10, 20, 5, DEFAULT_DURATION),
)


# Description displayed in the Scripts dialog window
def script_description():
    return """FART ON YOUR VIEWERS!
    
Finally, a script to facilitate hours of fantastic fecal funny foibles!
Configure a hotkey in Settings > Hotkeys and get to farting!"""


# Called at script unload
def script_unload():
    pass


# Called to set default values of data settings
def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "source_name", "")
    obs.obs_data_set_default_int(settings, "amplitude", DEFAULT_AMPLITUDE)
    obs.obs_data_set_default_double(settings, "frequency", DEFAULT_FREQUENCY)
    obs.obs_data_set_default_double(settings, "duration", DEFAULT_DURATION)


# Fills the given list property object with the names of all sources plus an empty one
def populate_list_property_with_source_names(list_property):
    sources = obs.obs_enum_sources()
    obs.obs_property_list_clear(list_property)
    obs.obs_property_list_add_string(list_property, "", "")
    for source in sources:
        name = obs.obs_source_get_name(source)
        obs.obs_property_list_add_string(list_property, name, name)
    obs.source_list_release(sources)


# Called to display the properties GUI
def script_properties():
    props = obs.obs_properties_create()

    # Drop-down list of sources
    source_list = obs.obs_properties_add_list(
        props,
        "source_name",
        "Source to fart on",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING,
    )
    populate_list_property_with_source_names(source_list)

    # Button to refresh the drop-down list
    obs.obs_properties_add_button(
        props,
        "button",
        "Refresh list of sources",
        lambda props, prop: True
        if populate_list_property_with_source_names(source_list)
        else True,
    )

    obs.obs_properties_add_float_slider(
        props, "frequency", "Wobble Speed", 0.1, 150, 0.1
    )
    obs.obs_properties_add_int_slider(props, "amplitude", "Wobble Intensity", 0, 100, 1)
    obs.obs_properties_add_float_slider(
        props, "duration", "Wobble Duration", 1, 3, 0.02
    )
    obs.obs_properties_add_float_slider(
        props, "scale_factor", "Scale Intensity", 0, 2, 0.01
    )
    obs.obs_properties_add_float_slider(
        props, "pos_factor", "Discombobulation", 0, 10000, 1
    )
    return props


# Called after change of settings including once after script load
def script_update(settings):
    source_name = obs.obs_data_get_string(settings, "source_name")
    amplitude = obs.obs_data_get_int(settings, "amplitude")
    frequency = obs.obs_data_get_double(settings, "frequency")
    duration = obs.obs_data_get_int(settings, "duration")
    scale_factor = obs.obs_data_get_double(settings, "scale_factor")
    pos_factor = obs.obs_data_get_double(settings, "pos_factor")
    shaker.set_source(source_name)
    shaker.set_wobble(
        Wobble(
            amplitude=amplitude,
            frequency=frequency,
            damping_factor=20 / duration,
            duration_seconds=duration,
        )
    )
    shaker.set_bulge(
        Bulge(
            amplitude=scale_factor,
            damping_factor=30 / duration,
            duration_seconds=duration,
        )
    )
    shaker.set_rattle(
        PlanarShake(
            amplitude=pos_factor,
            frequency=frequency / 1000,
            damping_factor=20 / duration,
            duration_seconds=duration,
        )
    )


# Called every frame
def script_tick(seconds):
    if shaker.start_time or shaker.trigger:
        shaker.shake()


# Callback for the hotkey
def on_shake_hotkey(pressed):
    shaker.trigger = pressed


# Called at script load
def script_load(settings):
    hotkey.id = obs.obs_hotkey_register_frontend(
        script_path(), "Fart Shake", on_shake_hotkey
    )
    hotkey_save_array = obs.obs_data_get_array(settings, "shake_hotkey")
    obs.obs_hotkey_load(hotkey.id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)


# Called before data settings are saved
def script_save(settings):
    obs.obs_save_sources()

    # Hotkey save
    hotkey_save_array = obs.obs_hotkey_save(hotkey.id)
    obs.obs_data_set_array(settings, "shake_hotkey", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
