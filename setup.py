from setuptools import find_packages, setup
from typing import List

HYPHEN ='-e .'

def get_requirements(path:str)->List[str]:
    '''
    This function returns the list of requirements to install this package
    '''
    requirements = []
    with open(path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('\n', '') for req in requirements]

        if HYPHEN  in requirements:
            requirements.remove(HYPHEN)
    
    return requirements




setup(
name = 'mlproject',
version = '0.0.1',
author = "Athon",
author_email = "athon_f@yahoo.com.br",
packages=find_packages(),
install_requires= get_requirements('requirements.txt')

)
