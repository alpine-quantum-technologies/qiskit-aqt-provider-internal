# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


from qiskit.providers.providerutils import filter_backends

from .aqt_backend import AQTSimulator, AQTSimulatorNoise1, AQTDevice, AQTDeviceIbex


class AQTProvider():
    """Provider for backends from Alpine Quantum Technologies (AQT)."""

    def __init__(self, access_token):
        super().__init__()

        self.access_token = access_token
        self.name = 'aqt_provider'
        # Populate the list of AQT backends
        self.backends = BackendService([AQTSimulator(provider=self),
                                        AQTSimulatorNoise1(provider=self),
                                        AQTDevice(provider=self),
                                        AQTDeviceIbex(provider=self)])

    def __str__(self):
        return "<AQTProvider(name={})>".format(self.name)

    def __repr__(self):
        return self.__str__()


class BackendService():
    """A service class that allows for autocompletion
    of backends from provider.
    """

    def __init__(self, backends):
        """Initialize service

        Parameters:
            backends (list): List of backend instances.
        """
        self._backends = backends
        for backend in backends:
            setattr(self, backend.name(), backend)

    def __call__(self, name=None, filters=None, **kwargs):
        """A listing of all backends from this provider.

        Parameters:
            name (str): The name of a given backend.
            filters (callable): A filter function.

        Returns:
            list: A list of backends, if any.
        """
        # pylint: disable=arguments-differ
        backends = self._backends
        if name:
            backends = [
                backend for backend in backends if backend.name() == name]

        return filter_backends(backends, filters=filters, **kwargs)
