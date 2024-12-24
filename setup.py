import os
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class BuildCppWithCMake(build_ext):
    def run(self):
        print("Starting of run command of pyplot_orientedmap")
        repo_url = "/Users/mathieu/GITall/GIT/Plot_orientedmap"
        clone_dir = "cpp_code_repo"

        if not os.path.exists(clone_dir):
            print(f"Cloning repository from {repo_url}...")
            subprocess.check_call(['git', 'clone', '--recursive', repo_url, clone_dir])

        # Step 2: Run CMake to build the C++ project
        build_dir = os.path.join(clone_dir, 'build')
        print("build_dir=", build_dir)

        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        print("Configuring CMake project...")
        subprocess.check_call(['cmake', '..'], cwd=build_dir)

        print("Building the C++ code...")
        subprocess.check_call(['cmake', '--build', '.'], cwd=build_dir)

        target_bin_dir = os.path.join(self.build_lib, 'pyplot_orientedmap', 'bin')
        print("target_bin_dir=", target_bin_dir)
        if not os.path.exists(target_bin_dir):
            print("Creating target_bin_dir=", target_bin_dir)
            os.makedirs(target_bin_dir)

        # Step 3: Copy the generated binaries (artifacts) to the Python package directory
        binaries = ["CombPlaneToSVG"]

        print("Copying the binaries ...")
        for binary in binaries:
            # Assuming the binaries are located in the 'build' directory
            the_binary = os.path.join(build_dir, binary)
            print("the_binary=", the_binary)
            if os.path.exists(the_binary):
                subprocess.check_call(['cp', the_binary, target_bin_dir])
            else:
                raise FileNotFoundError(f"Error: {binary} was not found in {build_dir}")
        print("After the execution of the run command")

cpp_extension = Extension(
    'my_cpp_extension',
    sources=[],  # We are building the C++ code separately using CMake
)

setup(
    name='pyplot_orientedmap',
    version='0.1.0',
    packages=['pyplot_orientedmap'],
    ext_modules=[cpp_extension],
    cmdclass={
        'build_ext': BuildCppWithCMake,  # Use the custom command to build the C++ code
    },
    package_data={
        'pyplot_orientedmap': ['bin/*'],  # Ensure binaries are included in the package
    },
    # Add any Python dependencies here
    install_requires=[],
)
