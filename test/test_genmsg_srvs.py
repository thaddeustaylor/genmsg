# Software License Agreement (BSD License)
#
# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import sys

def get_test_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))

def test_SrvSpec():
    from genmsg import MsgSpec, SrvSpec

    types = ['int32']
    names = ['a']
    constants = []
    text = 'int32 a'
    msg_a = MsgSpec(types, names, constants, text)

    types = ['int64']
    names = ['b']
    constants = []
    text = 'int64 b'
    msg_b = MsgSpec(types, names, constants, text)

    text = msg_a.text + '\n---\n' + msg_b.text
    spec = SrvSpec(msg_a, msg_b, text)
    assert msg_a == spec.request
    assert msg_b == spec.response
    assert text == spec.text
    assert '' == spec.full_name
    assert '' == spec.short_name
    assert '' == spec.package
        
    # tripwire
    assert repr(spec)
    assert str(spec)

    # exercise eq
    assert spec != 'spec'
    assert not spec == 'spec'
        
    spec2 = SrvSpec(msg_a, msg_b, text)
    assert spec == spec2
    assert not spec != spec2
        
    # - full_name
    spec2.full_name = 'something'
    assert spec != spec2
    spec2.full_name = ''        
    assert spec == spec2

    # - short_name
    spec2.short_name = 'something'
    assert spec != spec2
    spec2.short_name = ''        
    assert spec == spec2
    # - package
    spec2.package = 'something'
    assert spec != spec2
    spec2.package = ''        
    assert spec == spec2
        
def test_load_from_file():
    from genmsg.msgs import MsgContext
    from genmsg.srvs import load_from_file
        
    msg_context = MsgContext.create_default()
    
    d = get_test_dir()
    filename = os.path.join(d, 'test_ros', 'srv', 'AddTwoInts.srv')
    with open(filename, 'r') as f:
        text = f.read()
        
    spec = load_from_file(msg_context, filename)
    assert ['int64', 'int64'] == spec.request.types, spec.request.types
    assert ['a', 'b'] == spec.request.names
    assert text == spec.text
    
    # test that package_context gets normalized
    spec2 = load_from_file(msg_context, filename, package_context='foo')
    spec2b = load_from_file(msg_context, filename, package_context='foo/')
    spec2c = load_from_file(msg_context, filename, package_context='foo//')

    assert spec2 == spec2b
    assert spec2 == spec2c    

