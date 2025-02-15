import mock

from leapp.libraries.actor import library
from leapp.libraries.common import testutils
from leapp.libraries.stdlib import api
from leapp.models import MemoryInfo


def test_with_low_memory(monkeypatch):
    with mock.patch("__builtin__.open", mock.mock_open(read_data="MemTotal: 42 kB")) as mock_proc_meminfo:
        monkeypatch.setattr(api, 'produce', testutils.produce_mocked())
        library.process()
        mock_proc_meminfo.assert_called_once_with('/proc/meminfo')
        assert api.produce.called == 1
        assert MemoryInfo(mem_total=42) == api.produce.model_instances[0]


def test_with_high_memory(monkeypatch):
    with mock.patch("__builtin__.open", mock.mock_open(read_data="MemTotal: 424242424242 kB")) as mock_proc_meminfo:
        monkeypatch.setattr(api, 'produce', testutils.produce_mocked())
        library.process()
        mock_proc_meminfo.assert_called_once_with('/proc/meminfo')
        assert api.produce.called == 1
        assert MemoryInfo(mem_total=424242424242) == api.produce.model_instances[0]
