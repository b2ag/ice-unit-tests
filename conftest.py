# -*- coding: utf-8 -*-

import pytest
import os
import requests
import socket
import subprocess
import tempfile
import json


def ice_process_setup( ice_executable, ice_options ):
 popen_arguments = sum([['--'+k,str(v)] for k,v in ice_options.items()],[ice_executable])
 print("Starting FAF ICE Adapter like this: {}".format(' '.join(popen_arguments)))
 ice_process = subprocess.Popen( popen_arguments )
 return ice_process  
def ice_process_teardown( ice_process ):
 print("Shutting down FAF ICE Adapter")
 if ice_process.poll() is None:
  ice_process.kill()
 try:
  ice_process.wait(3)
 except subprocess.TimeoutExpired:
  ice_process.terminate()

def simple_socket_setup( ip, port ):
 simple_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 simple_socket.connect(( ip, port ))
 simple_socket.settimeout(1)
 return simple_socket

def simple_socket_server_setup( ip, port ):
 simple_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 simple_socket.bind(( ip, port ))
 simple_socket.settimeout(1)
 return simple_socket

@pytest.fixture()
def ice_process( request ):
 ice_options = request.module.ice_options
 ice_executable = request.module.ice_executable
 ice_process = ice_process_setup( ice_executable, ice_options )
 yield ice_process
 ice_process_teardown( ice_process )

@pytest.fixture()
def rpc_client( request ):
 ice_options = request.module.ice_options
 rpc_client = False
 for i in range(10000):
  try:
   rpc_client = simple_socket_setup( '127.0.0.1', ice_options['rpc-port'] )
   break
  except ConnectionRefusedError:
   pass
 yield rpc_client
 rpc_client.close()

@pytest.fixture()
def gpgnet_gameside( request ):
 ice_options = request.module.ice_options
 gpgnet_gameside = simple_socket_setup( '127.0.0.1', ice_options['gpgnet-port'] )
 yield gpgnet_gameside
 gpgnet_gameside.close()

@pytest.fixture()
def peer_traffic_gameside( request ):
 ice_options = request.module.ice_options
 peer_traffic_gameside = simple_socket_server_setup( '0.0.0.0', ice_options['lobby-port'] )
 yield peer_traffic_gameside
 peer_traffic_gameside.close()

@pytest.fixture()
def ice_2nd_process( request ):
 ice_options = request.module.ice_2nd_instance_options
 ice_executable = request.module.ice_executable
 ice_process = ice_process_setup( ice_executable, ice_options )
 yield ice_process
 ice_process_teardown( ice_process )

@pytest.fixture()
def rpc_2nd_client( request ):
 ice_options = request.module.ice_2nd_instance_options
 rpc_client = False
 for i in range(10000):
  try:
   rpc_client = simple_socket_setup( '127.0.0.1', ice_options['rpc-port'] )
   break
  except ConnectionRefusedError:
   pass
 yield rpc_client
 rpc_client.close()

@pytest.fixture()
def gpgnet_2nd_gameside( request ):
 ice_options = request.module.ice_2nd_instance_options
 gpgnet_gameside = simple_socket_setup( '127.0.0.1', ice_options['gpgnet-port'] )
 yield gpgnet_gameside
 gpgnet_gameside.close()

@pytest.fixture()
def peer_traffic_2nd_gameside( request ):
 ice_options = request.module.ice_2nd_instance_options
 peer_traffic_gameside = simple_socket_server_setup( '0.0.0.0', ice_options['lobby-port'] )
 yield peer_traffic_gameside
 peer_traffic_gameside.close()


