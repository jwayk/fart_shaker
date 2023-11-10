import obspython as obs


def get_source_from_current_scene(source_name: str):
  current_scene_source = obs.obs_frontend_get_current_scene()

  if not current_scene_source:
    return None
  
  current_scene = obs.obs_scene_from_source(current_scene_source)
  scene_item = obs.obs_scene_find_source_recursive(current_scene, source_name)
  obs.obs_source_release(current_scene_source)
  return scene_item
