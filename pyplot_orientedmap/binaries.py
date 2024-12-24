import os
import ast
import subprocess
import tempfile

def get_binary_path(the_bin):
    """
    Gets the binary to use for the computation
    """
    # Get the directory of the current file (inside the package)
    bin_dir = os.path.join(os.path.dirname(__file__), 'bin')
    binary_path = os.path.join(bin_dir, the_bin)
    if not os.path.exists(binary_path):
        raise FileNotFoundError(f"Binary {binary_path} not found in {bin_dir}")
    return binary_path

def write_invers_next_file(file_name, l_next, l_invers):
    n_de = len(l_next)
    f = open(file_name, 'w')
    f.write(str(n_de) + '\n')
    for i_de in range(n_de):
        f.write(" " + str(l_invers[i_de]))
    f.write("\n")
    for i_de in range(n_de):
        f.write(" " + str(l_next[i_de]))
    f.write("\n")
    f.close()


def write_namelist_file(input_file, plane_file, svg_file):
    f = open(input_file, 'w')
    f.write("&PLOT\n")
    f.write(" PlaneFile = \"" + plane_file + "\"\n")
    f.write(" OutFile = \"" + svg_file + "\"\n")
    f.write(" MAX_ITER_PrimalDual = -1\n")
    f.write(" MAX_ITER_CaGe = 1000\n")
    f.write(" CaGeProcessPolicy = 2\n")
    f.write(" RoundMethod = 2\n")
    f.write(" width = 600\n")
    f.write(" height = 600\n")
    f.write(" MethodInsert = 2\n")
    f.write(" ListExportFormat = \"eps\"")
    f.write("/\n")
    f.write("\n")
    f.write("&EDGE\n")
    f.write(" DoMethod1 = .T.\n")
    f.write(" DoMethod2 = .F.\n")
    f.write(" DoMethod3 = .F.\n")
    f.write(" MultTangent = 0.5\n")
    f.write(" NormalTraitSize = 1\n")
    f.write(" ListTraitIDE = \n")
    f.write(" ListTraitGroup = \n")
    f.write(" ListTraitSize = 6\n")
    f.write(" DefaultRGB = 0,0,0\n")
    f.write(" SpecificRGB_iDE = \n")
    f.write(" SpecificRGB_Group = \n")
    f.write(" SpecificRGB_R = \n")
    f.write(" SpecificRGB_G = \n")
    f.write(" SpecificRGB_B = \n")
    f.write("/\n")
    f.write("&VERT\n")
    f.write(" ListRadiusIDE = \n")
    f.write(" ListRadiusGroup = \n")
    f.write(" ListRadius = \n")
    f.write(" DefaultRGB = 0,0,0\n")
    f.write(" SpecificRGB_iDE = \n")
    f.write(" SpecificRGB_Group = \n")
    f.write(" SpecificRGB_R = \n")
    f.write(" SpecificRGB_G = \n")
    f.write(" SpecificRGB_B = \n")
    f.write("/\n")
    f.write("\n")
    f.write("&TORUS\n")
    f.write(" minimal = 1e-11\n")
    f.write(" tol = 1e-05\n")
    f.write(" AngDeg = 0\n")
    f.write(" scal = 0.8\n")
    f.write(" shiftX = 0\n")
    f.write(" shiftY = 0\n")
    f.write(" FundamentalRGB = 255,0,0\n")
    f.write(" FundamentalTraitSize = 2\n")
    f.write(" DrawFundamentalDomain = .T.\n")
    f.write("/\n")
    f.close()

def run_and_check(list_comm):
    """
    Run a command and process what is happening. Stop if an error is detected
    """
    result = subprocess.run(list_comm, capture_output=True, text=True)
    if result.returncode != 0:
        print("result=", result)
        print("returncode=", result.returncode)
        print("list_comm=", list_comm)
        raise RuntimeError("The running of the program went wrongly")

def draw_svg_file(l_next, l_invers, svg_file):
    """
    Draws the coordinate from the invers/next operations.
    :param l_invers, the permutation of the directed edges from the invers operator
    :param l_next, the permutation of the directed edges from the next operator
    :return: The output as a file.
    """
    binary_path = get_binary_path("CombPlaneToSVG")
    namelist_input = tempfile.NamedTemporaryFile()
    plane_input = tempfile.NamedTemporaryFile()
    namelist_file = namelist_input.name
    plane_file = plane_input.name
    write_invers_next_file(plane_file, l_next, l_invers)
    write_namelist_file(namelist_file, plane_file, svg_file)
    run_and_check([binary_path, namelist_file])
