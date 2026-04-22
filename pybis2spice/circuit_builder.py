from . import subcircuit as sckt
from .data_model import DataModel

from typing import Literal

_CORNER = Literal['Typical', 'WeakSlow', 'FastStrong']

def generate_spice_model(
        io_type: str, subcircuit_type:str, ibis_data: DataModel, 
        corner: _CORNER, output_filepath: str, truncation: int
        ):
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
    try:
        spice_str = ''
        if io_type == "Output":
            if subcircuit_type == "Generic":
                spice_str = sckt.create_generic_output_model(ibis_data, corner, io_type, truncation)

            if subcircuit_type == "LTSpice":
                spice_str = sckt.create_ltspice_output_model(ibis_data, corner, io_type, truncation)

            if subcircuit_type == "ngSPICE":
                spice_str = sckt.create_ngspice_output_model(ibis_data, corner, io_type, truncation)

        if io_type == "Input":
            spice_str = sckt.create_input_model(ibis_data, corner, io_type, ng=subcircuit_type=="ngSPICE")

        with open(output_filepath, 'w+') as file:
            file.write(spice_str)
            return output_filepath
    except Exception as e:
        raise e

def generate_diff_spice_model(
        io_type: str, subcircuit_type:str, ibis_data_p1: DataModel, 
        ibis_data_p2: DataModel, corner: _CORNER, output_filepath: str, 
        truncation: int
        ):
    try:
        spice_str = ''
        if io_type == "Output":

            if subcircuit_type == "Generic":
                spice_str = sckt.create_generic_output_model(ibis_data_p1, corner, io_type, truncation)
                spice_str += sckt.create_generic_output_model(ibis_data_p2, corner, io_type, truncation)

            if subcircuit_type == "LTSpice":
                spice_str = sckt.create_ltspice_output_model(ibis_data_p1, corner, io_type, truncation)
                spice_str += sckt.create_ltspice_output_model(ibis_data_p2, corner, io_type, truncation)

            if subcircuit_type == "ngSPICE":
                spice_str = sckt.create_ngspice_output_model(ibis_data_p1, corner, io_type, truncation)
                spice_str += sckt.create_ngspice_output_model(ibis_data_p2, corner, io_type, truncation)
                spice_str += '.if (stimulus%2==0)\n\n'
                spice_str += '.param stimulus_inv = stimulus-1\n\n'
                spice_str += '.else\n\n'
                spice_str += '.param stimulus_inv = stimulus+1\n\n'
                spice_str += f'.SUBCKT diff_{ibis_data_p1.model_name}_{ibis_data_p2.model_name}_{corner}_{io_type}'
                spice_str += 'OUT INV_OUT stimulus=1 freq=10Meg duty=0.5 delay=0 \n\n'
                spice_str += f'X1 OUT1 {ibis_data_p1.model_name}_{io_type}_{corner}'
                spice_str += 'stimulus={{stimulus}} freq={{freq}} duty={{duty}} delay={{delay}}\n\n'
                spice_str += f'X2 INV_OUT {ibis_data_p2.model_name}_{io_type}_{corner}'
                spice_str += 'stimulus={{stimulus_inv}} freq={{freq}} duty={{duty}} delay={{delay}}\n\n'
                spice_str += '.ENDS'                

        if io_type == "Input":
            spice_str = sckt.create_input_model(ibis_data_p1, corner, io_type, ng=subcircuit_type=="ngSPICE")
            spice_str += sckt.create_input_model(ibis_data_p2, corner, io_type, ng=subcircuit_type=="ngSPICE")
        
        with open(output_filepath, 'w+') as file:
                file.write(spice_str)
                return output_filepath
    except Exception as e:
        raise e
