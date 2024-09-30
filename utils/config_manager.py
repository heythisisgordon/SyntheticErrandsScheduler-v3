"""
Configuration Manager for the Synthetic Errands Scheduler

This module is responsible for loading, providing access to, and updating the configuration
settings defined in the config.yaml file. It uses the PyYAML library to parse
the YAML configuration file and provides a simple interface to access and modify the
configuration values.

Usage:
    from utils.config_manager import config
    
    # Access configuration values
    num_customers = config.get('default_num_customers')
    work_start_time = config.get('work_start_time')

    # Update configuration values
    config.update({'default_num_customers': 15})
    config.save()

The ConfigManager class is a singleton, ensuring that only one instance of the
configuration is loaded and used throughout the application.
"""

import yaml
from typing import Any, Dict, Optional

class ConfigManager:
    """
    A singleton class for managing configuration settings.
    
    This class loads the configuration from a YAML file and provides
    methods to access and update the configuration values.
    """
    
    _instance = None
    _config: Dict[str, Any]
    _config_file: str = 'config.yaml'
    
    def __new__(cls) -> 'ConfigManager':
        """
        Create a new instance of ConfigManager if it doesn't exist,
        otherwise return the existing instance.
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self) -> None:
        """
        Load the configuration from the config.yaml file.
        
        This method is called when the ConfigManager instance is first created.
        It reads the YAML file and stores the configuration in memory.
        """
        with open(self._config_file, 'r') as config_file:
            self._config = yaml.safe_load(config_file)
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value by its key.
        
        Args:
            key (str): The configuration key to look up.
            default (Optional[Any], optional): The default value to return if the key is not found.
        
        Returns:
            Any: The value associated with the key, or the default value if not found.
        """
        return self._config.get(key, default)
    
    def get_errand_type(self, errand_name: str) -> Dict[str, Any]:
        """
        Get the configuration for a specific errand type.
        
        Args:
            errand_name (str): The name of the errand type to look up.
        
        Returns:
            Dict[str, Any]: A dictionary containing the configuration for the specified errand type.
                            Returns an empty dictionary if the errand type is not found.
        """
        errand_types = self.get('errand_types', [])
        for errand_type in errand_types:
            if errand_type['name'] == errand_name:
                return errand_type
        return {}

    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update the configuration with new values.

        Args:
            updates (Dict[str, Any]): A dictionary containing the keys and values to update.
        """
        self._config.update(updates)

    def save(self) -> None:
        """
        Save the current configuration to the config.yaml file.
        """
        with open(self._config_file, 'w') as config_file:
            yaml.dump(self._config, config_file, default_flow_style=False)

# Create a global instance of ConfigManager
config = ConfigManager()