"""
Test submitting a VaspBaseWf workflow.

This does not seem to work, for `submit` the daemon will not pick up the workchain
and `run` just seems to get stuck after a while.
"""
# pylint: disable=unused-import,wildcard-import,unused-wildcard-import,unused-argument,redefined-outer-name
import time
import os
import subprocess as sp

import pytest
from aiida.common.extendeddicts import AttributeDict

from aiida_vasp.utils.fixtures import *
from aiida_vasp.utils.fixtures.data import POTCAR_FAMILY_NAME, POTCAR_MAP
from aiida_vasp.utils.aiida_utils import get_data_node


@pytest.mark.xfail()
def test_base(vasp_params, potentials, vasp_kpoints, vasp_structure, mock_vasp):
    """Test submitting only, not correctness, with mocked vasp code."""
    from aiida.orm import WorkflowFactory, Code, load_node
    from aiida.work import submit  # , run
    from aiida.work.db_types import Str

    base_wf_proc = WorkflowFactory('vasp.base')

    mock_vasp.store()

    os_env = os.environ.copy()
    sp.call(['verdi', 'daemon', 'start'], env=os_env)
    print sp.check_output(['verdi', 'daemon', 'status'], env=os_env)
    print sp.check_output(['which', 'verdi'], env=os_env)

    kpoints, _ = vasp_kpoints
    inputs = AttributeDict()
    inputs.code = Code.get_from_string('mock-vasp@localhost')
    inputs.structure = vasp_structure
    inputs.incar = vasp_params
    inputs.kpoints = kpoints
    inputs.potcar_family = Str(POTCAR_FAMILY_NAME)
    inputs.potcar_mapping = get_data_node('parameter', dict=POTCAR_MAP)
    inputs.options = get_data_node(
        'parameter', dict={
            'queue_name': 'None',
            'resources': {
                'num_machines': 1,
                'num_mpiprocs_per_machine': 1
            }
        })

    # ~ workchain = run(base_wf_proc, **inputs)
    running = submit(base_wf_proc, **inputs)
    workchain = load_node(running.pk)
    timeout = 5
    waiting_for = 0
    while not workchain.is_terminated and waiting_for < timeout:
        time.sleep(1)
        waiting_for += 1
    assert workchain.is_terminated
    assert workchain.is_finished_ok
