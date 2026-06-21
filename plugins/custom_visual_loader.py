import importlib
import os

class PluginManager:
    def __init__(self, plugin_dir='plugins/visuals'):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(self.plugin_dir, filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'VisualPlugin'):
                    self.plugins[module_name] = module.VisualPlugin()
        return self.plugins