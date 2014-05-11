import os
import yaml

from .inherited_config import InheritedConfig


__all__ = ['config']


local_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(local_dir, 'default_config.yaml')) as f:
    config = InheritedConfig(yaml.load(f))
