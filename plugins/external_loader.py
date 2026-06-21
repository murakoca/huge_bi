import importlib
import pkg_resources
import os

class ExternalPluginManager:
    def __init__(self, plugin_names=None):
        # plugin_names: pip paket adları listesi
        self.plugins = {}
        if plugin_names:
            for name in plugin_names:
                self.load_pip_plugin(name)

    def load_pip_plugin(self, package_name):
        try:
            mod = importlib.import_module(package_name)
            if hasattr(mod, 'register_visual'):
                visuals = mod.register_visual()
                self.plugins[package_name] = visuals
                print(f"Eklenti yüklendi: {package_name}")
        except Exception as e:
            print(f"Eklenti yüklenemedi: {package_name} - {e}")