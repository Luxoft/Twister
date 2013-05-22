
/**
*
* version: 1.000
*
* -*- coding: utf-8 -*-
*
* File: ExternalVariableType.java ; This file is part of Twister.
*
* Copyright (C) 2012 , Luxoft
*
* Authors:
*    Adrian Toader <adtoader@luxoft.com>
*
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at:
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
*/


// Java interface for a external variable object




package tscJython.interfaces;


import org.python.core.PyObject;




public interface ExternalVariableType {

    public void logMessage(String message);
    public boolean setVariable(String name, int value);
    public PyObject getVariable(String name);

}
