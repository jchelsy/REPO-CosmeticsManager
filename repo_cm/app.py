import os
from . import helpers as util

userprofile = os.getenv('USERPROFILE')
appdata = os.getenv('APPDATA')


# NOTE: Folder Structure
# MOD MANAGER PATH:  "...\com.kesomannen.gale\repo"
# PROFILE DIRECTORY:                          "...\profiles"
# EACH PROFILE (list):                                 "...\[PROFILE_NAME]"
# EACH PROFILE'S MODS:                                 "...\[PROFILE_NAME]\BepInEx\plugins\"
# 
# WITHIN EACH PROFILE:
# ====================
# ALL MOD FOLDERS (list):                                                             "...\[MOD_NAME]"


class CosmeticManager:
    def __init__(self, mod_manager_path: str):
        self.__mod_manager_path = mod_manager_path
        self.profiles_path = os.path.join(mod_manager_path, "profiles")
        # self._profiles = util.get_subdirectories(self.profiles_path)
        
        self.__mods = []
        
        self.initialize()
    
    def initialize(self):
        cosmetic_mods = []
        for profile in util.get_subdirectories(self.profiles_path):
            cosmetic_mods.append(self.retrieve_profile_mods(profile, True))
        
        for profile in cosmetic_mods:
            for mod in profile:
                self.__mods.append(CosmeticMod(mod))
    
    @staticmethod
    def retrieve_profile_mods(profile_path: str, cosmetic_only: bool = False) -> list:
        """Retrieves a list of all mod folders within a profile.
        - If `cosmetic_only` parameter is True:
          - Then, limit the criteria to only mods that contain cosmetic (.hhh) files.

        Args:
            profile_path (str): Root directory of a profile.
            cosmetic_only (bool, optional): If `True`, only retrieve mods that have cosmetics! Defaults to False.

        Returns:
            list: A list of all mods within `profile_path` that meet the given criteria (if applicable).
        """
        
        # Path containing all mod folders
        plugins_path = os.path.join(profile_path, "BepInEx", "plugins")
        
        return [os.path.join(plugins_path, mod) for mod in util.get_subdirectories(plugins_path) if not cosmetic_only or util.has_cosmetic(mod)]
    
    @staticmethod
    def retrieve_all_cosmetics(profile_path: str) -> list:
        """Retrieves all cosmetic (.hhh) model files within a profile.

        Args:
            profile_path (str): Root directory to begin the scan.

        Returns:
            list: A list of ALL `*.hhh` files found anywhere within `profile_path`.
        """
        
        file_list = []
        
        for root, dirs, files in os.walk(profile_path):
            for file in files:
                if file.endswith(".hhh"):
                    file_list.append(os.path.join(root, file))
        return file_list
    
    def get_mm_path(self) -> str:
        return self.__mod_manager_path
    def set_mm_path(self, new_path: str):
        self.__mod_manager_path = new_path
    mm_path = property(get_mm_path, set_mm_path)
    
    def get_mods(self) -> list:
        return self.__mods


class CosmeticMod:
    def __init__(self, path):
        self.path = path
        self.name = self.__str__()
        self.profile = util.go_up_path(self.path, 3)
    
    def __str__(self):
        return str(os.path.basename(self.path))


def run():
    test()  # For now, I'm only testing functions & Class implementation.


def test():
    # A temp folder to mimic the structure of Gale's root directory.
    #   (equivalent to: '...\com.kesomannen.gale\repo')
    test_start_dir = os.path.join(userprofile, "Documents", "TESTrepo")
    
    manager = CosmeticManager(test_start_dir)
    
    """Test output for CosmeticMod class functionality"""
    for item in manager.get_mods():
        print(os.path.basename(item.profile), ": ", item.path)
