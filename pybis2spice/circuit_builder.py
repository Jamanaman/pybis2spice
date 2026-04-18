from . import subcircuit as sckt
from .data_model import DataModel


def generate_spice_model(io_type: str, subcircuit_type:str, ibis_data: DataModel, corner: str, output_filepath: str, truncation: float):
    """
    Wrapper around the subcircuit file creation functions. Calls the relevant function i.e. LTSpice or Generic

        Parameters:
            io_type - "Input" or "Output" or "Tri-State
            subcircuit_type - "LTSpice" or "Generic"
            ibis_data - a DataModel object (defined in pybis2spice.py)
            corner - "WeakSlow" or "Typical" or "FastStrong"
            output_filepath - path of output file
            truncation - the percentage of the total range to use to truncate trailing samples in rising and falling waveforms

        Returns:
            The path of the created file
    """
    ret = None
    if io_type == "Output":

        if subcircuit_type == "Generic":
            ret = sckt.create_generic_output_model(ibis_data, corner, io_type, output_filepath, truncation)

        if subcircuit_type == "LTSpice":
            ret = sckt.create_ltspice_output_model(ibis_data, corner, io_type, output_filepath, truncation)

        if subcircuit_type == "ngSPICE":
            ret = sckt.create_ngspice_output_model(ibis_data, corner, io_type, output_filepath, truncation)

    if io_type == "Input":
        ret = sckt.create_input_model(ibis_data, corner, io_type, output_filepath, ng=subcircuit_type=="ngSPICE")

    return ret

def generate_diff_spice_model(io_type: str, subcircuit_type:str, ibis_data_p1: DataModel, ibis_data_p2: DataModel, corner: str, output_filepath: str, truncation: float):
    # TODO: separate out the generation of the model string itself so that it can be written to a file or directly into python for code generation
    ret = None
    if io_type == "Output":

        if subcircuit_type == "Generic":
            ret = sckt.create_generic_output_model(ibis_data, corner, io_type, output_filepath, truncation)

        if subcircuit_type == "LTSpice":
            ret = sckt.create_ltspice_output_model(ibis_data, corner, io_type, output_filepath, truncation)

        if subcircuit_type == "ngSPICE":
            ret = sckt.create_ngspice_output_model(ibis_data, corner, io_type, output_filepath, truncation)

    if io_type == "Input":
        ret = sckt.create_input_model(ibis_data, corner, io_type, output_filepath, ng=subcircuit_type=="ngSPICE")

    return ret